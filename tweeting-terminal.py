import tweepy,sys,os,webbrowser,wx
f=open("errors.log","a")
sys.stderr=f
def twihelp():
	print("Currently available commands:")
	print("Tweet <text>, tweet out to the twitter world.")
	print("search <user>, search twitter for a specified username.")
	print("shell, enter a shell where commands can be typed without relaunching the application for each command.")
def gettext(command):
	finaltext=""
	chunks=command.split(" ")
	for i in range(1,len(chunks)):
		finaltext+=chunks[i]
		if i!=len(chunks)-1:
			finaltext+=" "
	return finaltext
def inputbox(parent=None,caption="",message="",default_value=""):
	app=wx.App()
	app.MainLoop()
	dlg = wx.TextEntryDialog(parent, caption, message,value=default_value)
	dlg.ShowModal()
	result = dlg.GetValue()
	dlg.Destroy()
	return result
def stripNewLine(sample_list):
	converted_list=[]
	for element in sample_list:
		converted_list.append(element.strip())
	return converted_list
consumer_key="74hOaUVeytG41oI591yrFCgys"
consumer_secret="8yp8W6xlhpQtjykmZwP4VlqEgDTtqgINIBDPU7dnDNUueydZSQ"
def authorise():
	auth=tweepy.OAuthHandler(consumer_key,consumer_secret)
	if os.path.exists("config.txt"):
		f=open("config.txt","r")
		stuff=f.readlines()
		f.close()
		stuff=stripNewLine(stuff)
		access_token=stuff[0]
		access_secret=stuff[1]
		auth.set_access_token(access_token,access_secret)
		return auth
	else:
		redirect_url=auth.get_authorization_url()
		webbrowser.open(redirect_url)
		verifier=inputbox(caption="Enter the verification code",message="Verification code")
		auth.get_access_token(verifier)
		f=open("config.txt","w")
		f.write(auth.access_token+"\n")
		f.write(auth.access_token_secret)
		f.close()
		return auth
def tweetstuff(api,text,inshell):
	if inshell==True:
		text=gettext(text)
	api.update_status(text)
def twishell(api,shellfuncs):
	inshell=True
	os.system("title Tweeting terminal")
	command=""
	while command!="exit":
		command=input("Tweeting terminal>")
		chunks=command.split(" ")
		if command=="help":
			twihelp()
		elif chunks[0] in shellfuncs:
			shellfuncs[chunks[0]](api,command,inshell)
		elif command=="exit":
			sys.exit()
		else:
			print("Invalid command. Type help for a list of commands.")
def perform_search(api,user,inshell):
	if inshell==True:
		user=gettext(user)
	item=api.search_users(user)
	print("Name: "+item[0].name)
	print("Screen name: "+item[0].screen_name)
	print("Description: "+item[0].description)
def main():
	auth=authorise()
	inshell=False
	api=tweepy.API(auth)
	shellfuncs={"tweet":tweetstuff,"search":perform_search,"help":twihelp}
	if len(sys.argv)>=2:
		if sys.argv[1]=="tweet":
			tweetstuff(api,sys.argv[2],inshell)
		elif sys.argv[1]=="search":
			perform_search(api,sys.argv[2],inshell)
		elif sys.argv[1]=="shell":
			twishell(api,shellfuncs)
		elif sys.argv[1]=="help":
			twihelp()
	else:
		print("Invalid argument or not enough parameters.")
main()