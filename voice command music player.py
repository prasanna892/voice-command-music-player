import pygame                           # pip install pygame
import pyttsx3                          # pip install pyttsx3
import speech_recognition as sr         # pip install SpeechRecognition
import datetime
from pygame import mixer
from datetime import datetime
import os
import time
from mutagen.mp3 import MP3             # pip install mutagen
import time                     
from tkinter import *                   # pip install tk or tkinter
from threading import Thread

################################################
""" 
please do not quit it using windowes quit button
if you like this the program will rise TCL error
and the python stop processing use "QUIT" button 
which was found in tkinter use that button to 
quit the tkinter window or say "quit music 
player" to quit it
"""
################################################

###############################################################################
"""
important message:
     It can only play .mp3 formate songs and \n songs in given path folder only
"""
###############################################################################
print("""Guidelines:
    say 'play music' to run musics
    say 'next song' or 'change song' or 'next songs' or 'change songs' to skip the song fardward
    say 'before song' or 'previous song' or 'before songs' or 'previous songs' to skip song backward
    say 'pause song' or 'pause' to pause the song
    say 'unpause song' or 'resume song' or 'unpause' or 'resume' to unpause the song
    say 'rise volume' or 'rise sound' or 'raise volume' or 'raise sound' to raise volume
    say 'low volume' to low volume
    say 'mute volume' to mute volume
    say 'maximum volume' or 'max volume' to set maximum volume
    say 'middle volume' or 'mid volume' or 'normal volume' to set normal volume
    say 'stop music' or 'stop song' or 'quit music' or 'quit song' to quit the player
    say 'stop music player' or 'stop player' or 'quit music player' or 'quit player' to quit the player
    say 'end' to stop the program
    or press the button in music player to perform an action
""")

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)    
        print("Say that again please...")
        query = 'Nothing'
        return "None"
    return query

########################### song play ##########################
songindex=0
counter=66600
flag=1
resume=0
breakre='unbreak'
volume=0.5
curr_time="00:00"
currenttime="00:00"
song_length=0
songlength="00:00"
songpause='unpause'
song_folder_path=None
end_recursion=False
except_flag_s=True
# creating music play function
def mus():
    global songindex
    global flag
    global volume
    global songlength
    global currenttime
    global songpause
    global song_folder_path
    global end_recursion
    global song_length
    try: # trying to play song
        while True:
            global counter

            # checking it is a valid path or not
            if ":\\" in song_folder_path:
                # getting all files in user specified path      
                songs = os.listdir(song_folder_path)
                String = songs[songindex]
                last3=str(String[-4:])

                # checking it is a mp3 or not
                if last3=='.mp3' or last3=='.MP3':       
                    pygame.init() # installing pygame

                    # creating current time of song
                    tt = datetime.fromtimestamp(counter)
                    curtime=tt.strftime("%M%S")
                    currenttime=tt.strftime("%M:%S")        
                    z=int(curtime)

                    # getting song time length
                    songs = os.listdir(song_folder_path)
                    song_mut = MP3((song_folder_path+'\\'+str(songs[songindex])))
                    song_length = song_mut.info.length
                    converted_song_length = time.strftime('%M%S',time.gmtime(song_length))
                    songlength= time.strftime('%M:%S',time.gmtime(song_length))
                    x=int(converted_song_length)

                    # starting to load and play song 
                    if flag<=1:
                        print(songs[songindex])
                        print("song index=",songindex)
                        mixer.init() # installing mixer
                        mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading song

                        # setting song title
                        try:
                            songname=songs[songindex]
                            canvas.itemconfig("marquee",text=songname)
                        except:
                            pass
                        mixer.music.set_volume(volume) # setting song volume
                        print("volume=",volume)
                        mixer.music.play() # playing song
                        flag+=1

                    # this condition work untill song current length equal to song length
                    if z<=x:
                        if songpause=='unpause':
                            counter+=1
                        time.sleep(1)

                    # this condition work when song current length greater_or_equal to song length
                    if z>=x:
                        print(songs[songindex+1]) 
                        songindex+=1 # increasing songs list index
                        counter=66600 # re_setting counter
                        mixer.init() # installing mixer again
                        mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading next song
                        # setting song title
                        try:
                            songname=songs[songindex]
                            canvas.itemconfig("marquee",text=songname)
                        except:
                            pass
                        print("volume=",volume)
                        mixer.music.play() # playing next song
                        print("song index=",songindex)
                        break

                else: # if there is any error it show error missage and play next song
                    if end_recursion!=True:
                        print("error")
                        nextsong()
                    elif end_recursion==True:
                        if flag<=1:
                            flag+=1
                            print("there is no m p 3 formate songs in your specified folder path")
                            print("say \"restart music player\" to restart it and enter a valid m p 3 song folder path")
                            canvas.itemconfig("marquee",text="enter valid song folder path. say 'restart music player'") # showing error message in player
                    break
                break

            else: # if user specifed a in valid directory this get executed
                if flag<=1:
                    flag+=1
                    print("enter a valid path")
                    print("say \"restart music player\" to restart it and enter a valid m p 3 song folder path")
                    canvas.itemconfig("marquee",text="enter valid song folder path. say 'restart music player'") # showing error message in player

    # if above try statement get faild and when it found 'FileNotFoundError' this except statement get executed
    except FileNotFoundError as fe:
        global except_flag_s
        if except_flag_s==True:
            print(fe)
            canvas.itemconfig("marquee",text="enter valid song folder path. say 'restart music player'") # showing error message in player
            except_flag_s=False

    # if try found some another error then this statement get executed and print which error cause this then call next song to play
    except Exception as e:
        songindex+=1
        if except_flag_s==True:
            print("some error acquired reason:")
            print(e)
            canvas.itemconfig("marquee",text="enter valid song folder path. say 'restart music player'") # showing error message in player
            except_flag_s=False

# when this function is executed, it stop re() function
flag_button=False
def stopsong():
    global breakre
    global flag_button
    breakre='break'
    flag_button=True

# this function is used to repetedly call mus() function
song_path1="nothing"
def re():
    global breakre
    global counter
    global flag
    global volume
    global songpause
    global songlength
    global currenttime
    global songindex
    global song_folder_path
    global song_path1
    global song_found
    global end_recursion
    global except_flag_s

    songpause='unpause'
    end_recursion=False
    except_flag_s=True

    # this condition check if previously entered path is equalto new path
    if song_path1!=song_folder_path:
        song_path1=song_folder_path
        songindex=0
        song_found=0

    # this loop execute mus() function repetedly
    while True:
        global breakre
        #when you call stopsong() function this condiction get true 
        #and reset the below variable value then break the loop
        if breakre=='break':
            counter=66600
            breakre='unbreak'
            flag=1
            volume=0.5
            currenttime="00:00"
            songlength="00:00"
            break
        mus()

# this function call next song to load and play  
song_found=0
def nextsong():
    global counter
    global songindex
    global volume
    global song_folder_path
    global song_found
    global end_recursion

    # trying to play next song
    try:
        songindex+=1 # increasing songs list index
        counter=66600 # resetting counter

        # getting next song
        songs = os.listdir(song_folder_path)
        totalitem=len(songs)-1
        String = songs[songindex]
        last3=str(String[-4:])

        # when songs list totalitem equalto index songindex this condition get true and call first song
        if songindex==totalitem:
            songindex=-1
            if song_found==0:
                end_recursion=True
                
        # try to play next song
        try:
            # checking it is a mp3 or not
            if last3=='.mp3' or last3=='.MP3':
                song_found+=1 
                print(songs[songindex])
                print("song index=",songindex)
                mixer.init() # installing mixer again
                mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading next song 

                # re_setting song title
                try:
                            songname=songs[songindex]
                            canvas.itemconfig("marquee",text=songname)
                except:
                    pass

                print("volume=",volume)
                mixer.music.play() # playing next song
            else:
                if end_recursion!=True:
                    nextsong()

        except: # there is any error, this function call again 
            nextsong()

    # if above try statement get faild and when it found 'FileNotFoundError' this except statement get executed
    except FileNotFoundError as fe: 
        print(fe)
    
    except Exception as e:
        print(e)

# this function call previous song to load and play  
def previoussong():
    global counter
    global songindex
    global volume
    global song_folder_path
    global song_found
    global end_recursion

    # trying to play previous song
    try:
        songindex-=1 # decreasing songs list index
        counter=66600 # resetting counter

        # getting previous song
        songs = os.listdir(song_folder_path)
        totalitem=len(songs)-1
        minus_totalitem=int('-'+str(totalitem+1))

        # when songs list songindex smaller and equalto minus_totalitem index  this condition get true and call first song
        if songindex<=minus_totalitem:
            songindex=0
            if song_found==0:
                end_recursion=True
        String = songs[songindex]
        last3=str(String[-4:])

        # trying to play previous song
        try:
            # checking it is a mp3 or not
            if last3=='.mp3' or last3=='.MP3':
                song_found+=1 
                print(songs[songindex])
                print("song index=",songindex)
                mixer.init() # installing mixer again
                mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading previous song 

                # re_setting song title
                try:
                    songname=songs[songindex]
                    canvas.itemconfig("marquee",text=songname)
                except:
                    pass

                print("volume=",volume)
                mixer.music.play() # playing previous song 
            else:
                if end_recursion!=True:
                    previoussong()

        except: # there is any error, this function call again 
            previoussong()

    # if above try statement get faild and when it found 'FileNotFoundError' this except statement get executed
    except FileNotFoundError as fe:
        print(fe)

    except Exception as e:
        print(e)

# this function pause the playing song   
def pause():
    global counter
    global resume
    global songpause
    songpause='pause'
    resume = counter
    mixer.music.pause() 

# this function unpause the paused song 
def unpause():
    global counter
    global resume
    global songpause
    songpause='unpause'
    if songpause=='pause':
        counter = resume
    mixer.music.unpause()

# this function increase song volume
def rise_volume():
    global volume
    global vol2
    # setting max volume condition
    if volume<1.0:
        volume=round(volume,1)
        volume+=0.1
        volume=round(volume,1)

        # re_setting volume displayed in player
        try:
            text1=int(volume*10)
            vol2.config(text=(text1))
        except:
            pass

        print("volume=",volume)
        mixer.init()
        mixer.music.set_volume(volume)
        print("volume raised")
        speak("volume raised")
    if volume>=1.0:
        print("maximum volume reached \nno more volume is increasd")
        speak("maximum volume reached")
        speak("no more volume is increasd")

# same as above
def volumeup():
    global volume
    global vol2
    if volume<1.0:#0.9:
        volume=round(volume,1)
        volume+=0.1
        volume=round(volume,1)
        try:
            text1=int(volume*10)
            vol2.config(text=(text1))
        except:
            pass
        mixer.init()
        mixer.music.set_volume(volume)
    if volume>=1.0:#0.9:
        pass
        
# this function decrease song volume
def low_volume():
    global volume
    global vol2

    # setting min volume
    if volume>0.0:
        volume=round(volume,1)
        volume-=0.1
        volume=round(volume,1)

        # re_setting volume displayed in player
        try:
            text1=int(volume*10)
            vol2.config(text=(text1))
        except:
            pass

        print("volume=",volume)
        mixer.init()
        mixer.music.set_volume(volume)
        print("volume lowered")
        speak("volume lowered")
    if volume<=0.0:
        print("lower volume is reached \nvolume set as mute")
        speak("lower volume is reached")
        speak("volume set as mute")
        volume=0.0

# same as above
def volumedown():
    global volume
    global vol2
    if volume>0.0:
        volume=round(volume,1)
        volume-=0.1
        volume=round(volume,1)
        try:
            text1=int(volume*10)
            vol2.config(text=(text1))
        except:
            pass
        mixer.init()
        mixer.music.set_volume(volume)
       
    if volume<=0.0:
        volume=0.0

# this function set max volume
def max_volume():
    global volume
    global vol2
    volume=1.0

    # re_setting volume displayed in player
    try:
        text1=int(volume*10)
        vol2.config(text=(text1))
    except:
        pass

    print("volume=",volume)
    mixer.init()
    mixer.music.set_volume(volume)

# this function set middle volume
def mid_volume():
    global volume
    global vol2
    volume=0.5

    # re_setting volume displayed in player
    try:
        text1=int(volume*10)
        vol2.config(text=(text1))
    except:
        pass

    print("volume=",volume)
    mixer.init()
    mixer.music.set_volume(volume)

# this function set zero volume
def mute():
    global volume
    global vol2
    volume=0.0

    # re_setting volume displayed in player
    try:
        text1=int(volume)
        vol2.config(text=(text1))
    except:
        pass

    print("volume=",volume)
    mixer.init()
    mixer.music.set_volume(volume)

######################## song play end #########################

######################### music player #########################

# creating music player window
def music_player():
    global canvas
    global root
    global songindex
    global volume
    global curr_time
    global songlength
    global vol2
    global time2
    global flag_button
    global curtime
    global song_length
    global counter
    # this finction run the song title from right to left again and again
    def shift():
        x1,y1,x2,y2 = canvas.bbox("marquee")
        if(x2<0 or y1<0): #reset the coordinates
            x1 = canvas.winfo_width()
            y1 = canvas.winfo_height()//2
            canvas.coords("marquee",x1,y1)
        else:
            canvas.move("marquee", -2, 0)
        canvas.after(1000//fps,shift)
    ############# Main program ###############
    root=Tk() 
    width1= root.winfo_screenwidth() # getting your computer screen with           
    height1= root.winfo_screenheight() # getting over computer screen height 
    x=width1-487
    y=height1-215
    root.geometry(f'+{int(x)}+{int(y)}') # setting position for music player   
    root.maxsize(height=133,width=466) # setting max size for player
    root.title('Music player') # creating player title
    canvas=Canvas(root,bg='cyan3')

    # this function is used to get song folder path from user 
    def s_path():

        # which function is used to change test 
        def textch():
            global song_folder_path
            paths2.destroy()
            song_folder_path=entry1.get(1.0,"end-1c")
            entry1.destroy()
            msg.itemconfig("welcome",text=" NOW PLAYING:")
            msg.config(bg="blue",height=25,width=188) #420
            # calling re() function using thread 
            if __name__ == '__main__':
                Thread(target = re).start()  

            # creating slide value change function
            def slide_ch():
                rr=round(song_length)
                cc=counter-66600
                sl.config(to=int(rr))
                sl.set(int(cc))
                sl.after(200,slide_ch)

            # creating song len minus function
            def songm():
                global counter
                try: 
                    if counter>=66604:
                        counter-=3
                        songs = os.listdir(song_folder_path)
                        String = songs[songindex]
                        last3=str(String[-4:])
                        if last3=='.mp3' or last3=='.MP3':
                            mixer.init() # installing mixer again
                            mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading song 
                            mixer.music.play(start=counter-66600) # playing song minus 3 sec
                except:
                    pass

            # creating song len plus function
            def songp():
                global counter
                try:
                    if counter>=(song_length-2):
                        counter+=3
                        songs = os.listdir(song_folder_path)
                        String = songs[songindex]
                        last3=str(String[-4:])
                        if last3=='.mp3' or last3=='.MP3':
                            mixer.init() # installing mixer again
                            mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading song 
                            mixer.music.play(start=counter-66600) # playing song plus 3 sec
                except:
                    pass

            # creating song len minus button
            songminus=Button(frame1,text="-",font=("arial",10,"bold"),bg="MediumOrchid4",borderwidth=1,command=lambda:songm())
            songminus.pack(side=LEFT)

            # creating song len slider
            sl = Scale(frame1, from_=0, to=200, orient=HORIZONTAL,showvalue=0,length=200,background="violet",borderwidth=2,
            highlightbackground="white",highlightthickness=2,troughcolor="yellow",sliderlength=15)     # d:\song 224
            sl.set(0)
            sl.pack(side=LEFT)

            # creating song len plus button
            songplus=Button(frame1,text="+",font=("arial",10,"bold"),bg="MediumOrchid4",borderwidth=1,command=lambda:songp())
            songplus.pack(side=LEFT)
            slide_ch()

        # creating test frame to get input from user 
        entry1=Text(frame1,bg='yellow',height=1,width=25)
        msg.config(bg="blue",height=25,width=188)

        if flag_button==True:
            prepaths.destroy()
        newpaths.destroy()

        # creating 'ok' button 
        paths2=Button(frame1,text="OK",font=("arial",10,"bold"),bg="brown",borderwidth=1,command=lambda:textch())
        paths2.pack(side=RIGHT)
        entry1.pack(side=LEFT)
    
    # this function get previously entered song folder path from  user  
    def pre_path():
        global song_folder_path
        song_folder_path=song_folder_path

        # displaying error message when song folder path is equal to none 
        if song_folder_path==None:
            canvas.itemconfig("marquee",text="enter valid song folder path. say 'restart music player'")

        msg.itemconfig("welcome",text=" NOW PLAYING:")
        msg.config(bg="blue",height=25,width=188)

        # calling re() function using thread 
        if __name__ == '__main__':
            Thread(target = re).start()

        prepaths.destroy()
        newpaths.destroy()

        # creating slide value change function
        def slide_ch():
            rr=round(song_length)
            cc=counter-66600
            sl.config(to=int(rr))
            sl.set(int(cc))
            sl.after(200,slide_ch)

        # creating song len minus function
        def songm():
            global counter
            try: 
                if counter>=66604:
                    counter-=3
                    songs = os.listdir(song_folder_path)
                    String = songs[songindex]
                    last3=str(String[-4:])
                    if last3=='.mp3' or last3=='.MP3':
                        mixer.init() # installing mixer again
                        mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading song 
                        mixer.music.play(start=counter-66600) # playing song minus 3 sec
            except:
                pass

        # creating song len plus function
        def songp():
            global counter
            try:
                if counter>=(song_length-2):
                    counter+=3
                    songs = os.listdir(song_folder_path)
                    String = songs[songindex]
                    last3=str(String[-4:])
                    if last3=='.mp3' or last3=='.MP3':
                        mixer.init() # installing mixer again
                        mixer.music.load(os.path.join(song_folder_path,songs[songindex])) # loading song 
                        mixer.music.play(start=counter-66600) # playing song plus 3 sec
            except:
                pass

        # creating song len minus button
        songminus=Button(frame1,text="-",font=("arial",10,"bold"),bg="MediumOrchid4",borderwidth=1,command=lambda:songm())
        songminus.pack(side=LEFT)

        # creating song len slider
        sl = Scale(frame1, from_=0, to=200, orient=HORIZONTAL,showvalue=0,length=200,background="violet",borderwidth=2,
        highlightbackground="white",highlightthickness=2,troughcolor="yellow",sliderlength=15)     # d:\song 224
        sl.set(0)
        sl.pack(side=LEFT)

        # creating song len plus button
        songplus=Button(frame1,text="+",font=("arial",10,"bold"),bg="MediumOrchid4",borderwidth=1,command=lambda:songp())
        songplus.pack(side=LEFT)
        slide_ch()



    frame1=Frame(root)
    frame1.pack(side=TOP)
    msg = Canvas(frame1, bg="blue",height=25,width=264) #270
    msg.create_text(0,0,text="WELCOME",font=('Algerian',19,'italic'),fill='red',tags="welcome",anchor='nw')
    msg.pack(side=LEFT)

    # when help button is clicked this function get executed 
    def help():
        frame1.pack_forget()
        frame2.pack_forget()
        frame3=Frame(root)
        frame3.pack(side=TOP)

        # creating help text label 
        help_text1=Label(frame3,font=("arial",13,"bold"), text=" '<'next song, '>'pre song, '~'mute vol, '+'rise vol, '-'low vol,", fg="black",bg='green')
        help_text1.pack()
        help_text2=Label(frame3,font=("arial",13,"bold"), text=" 'play' play song, 'pause' pause song, 'QUIT' quit player ", fg="black",bg='green')
        help_text2.pack(side=LEFT)

        # when cancel button is clicked this function get executed  
        def recall():
            canvas.pack_forget()
            frame1.pack()
            canvas.pack(fill=BOTH, expand=1)
            frame2.pack()
            frame3.destroy()

        # creating cancel 'X' button 
        cancelx=Button(frame3,text=" X ",font=("arial",10,"bold"),bg="red",borderwidth=0,command=lambda:recall())
        cancelx.pack(side=RIGHT)

    # creating 'help' button 
    helps=Button(frame1,text="help",font=("arial",10,"bold"),bg="brown",borderwidth=1,command=lambda:help())
    helps.pack(side=RIGHT)

    # creating 'new path' button 
    newpaths=Button(frame1,text="Click to enter new path",font=("arial",10,"bold"),bg="red",borderwidth=1,command=lambda:s_path())
    newpaths.pack(side=RIGHT)

    if flag_button==True:
        msg.config(bg="blue",height=25,width=126)
        prepaths=Button(frame1,text="select previous path",font=("arial",10,"bold"),bg="red",borderwidth=1,command=lambda:pre_path())
        prepaths.pack(side=LEFT)

    # creating some information label to display 
    canvas.pack(fill=BOTH, expand=1)
    canvas.create_text(0,-2000,text="Enter song folder path",font=('Bauhaus 93',50,'bold'),fill='saddle brown',tags=("marquee",),anchor='w')#,text=text_var
    text2=f"{curr_time}/{songlength}"
    text1=int(volume*10)
    frame2=Frame(root)
    frame2.pack(side=BOTTOM)
    vol1= Label(frame2, font=("arial",13,"bold"), text=(" volume:"), fg="black",bg='green') 
    vol2= Label(frame2, font=("arial",13,"bold"), text=(text1), fg="black",bg='green')
    time1= Label(frame2, font=("arial",13,"bold"), text=("    time elapsed:"), fg="black",bg='green')
    time2= Label(frame2, font=("arial",13,"bold"), text=(text2), fg="black",bg='green')

    # creating previous song button 
    previouss=Button(frame2,text="<",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:previoussong())
    previouss.pack(side=LEFT)

    # creating volume up button 
    volups=Button(frame2,text="+",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:volumeup())
    volups.pack(side=LEFT)

    # when pause button is clicked this function get executed 
    def play_s():
        pause()
        pauses.pack_forget()

        # when play button is clicked this function get executed 
        def playes():
            unpause()
            plays.destroy()
            pauses.pack()
        plays=Button(frame2,text="plays",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:playes())
        plays.pack(side=RIGHT)

    # creating volume mute button
    volmutes=Button(frame2,text="~",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:mute())
    volmutes.pack(side=LEFT)

    # creating pause button 
    pauses=Button(frame2,text="pause",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:play_s())

    # creating volume decrease button  
    voldowns=Button(frame2,text="-",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:volumedown())
    voldowns.pack(side=LEFT)

    # creating next song button 
    nexts=Button(frame2,text=">",font=("arial",10,"bold"),bg="gold",borderwidth=0, command=lambda:nextsong())
    nexts.pack(side=LEFT)

    pauses.pack(side=LEFT)
    frame4=Frame(frame2)
    frame4.pack(side=RIGHT)

    # when quit button is clicked this function get executed 
    def quit_s():
        global flag_song
        global flag_song_start

        # trying to stop currently playing song 
        try:
            mixer.music.stop()
        except:
            pass

        # calling music_player_quit() and stopsong() function 
        music_player_quit()
        stopsong()
        flag_song=False
        flag_song_start=True

    # creating quote button to quit player 
    quits=Button(frame4,text="QUIT",font=("arial",10,"bold"),bg="red",borderwidth=0, command=lambda:quit_s())
    quits.pack(side=RIGHT)

    # packing some buttons and labels 
    time2.pack(side=RIGHT)
    time1.pack(side=RIGHT)
    vol2.pack(side=RIGHT)
    vol1.pack(side=RIGHT)

    # setting convex width and height 
    x1,y1,x2,y2 = canvas.bbox("marquee")
    #width = x2-x1
    height = y2-y1
    canvas['width']=300
    canvas['height']=height   #76
    fps=45    #Change the fps to make the animation faster/slower
    shift() # calling shift() function 

    # reacting song time function 
    # this function repeatedly update the song current time and song length 
    def songtime():
        text2=f"{currenttime}/{songlength}"
        time2.config(text=(text2))
        time2.after(100,songtime)
    songtime() # calling songtime() function 

    # closeing main loop 
    root.mainloop()
    
# this function is used to quit music player 
def music_player_quit():
    global root
    try:
        root.quit()
    except:
        pass
    
####################### music player end #######################


flag_song=False
flag_song_start=True
if __name__ == '__main__':
    speak('hello')
    while True:
        # getting voice input from user 
        query = takeCommand().lower()
        #query = input("     ")
        
        # creating if else statement to activate command
        if query =='play music':# or query=='z':
            if flag_song_start==True:
                mid_volume()

                # starting music_player() function using thread 
                if __name__ == '__main__':
                    Thread(target = music_player).start()

                flag_song=True
                flag_song_start=False
 
        elif query=='next song' or query=='change song' or query=='next songs' or query=='change songs':# or query=='n':
            if flag_song==True:
                print("song changed")
                speak("song changed")
                nextsong()
                        
        elif query=='before song' or query=='previous song' or query=='before songs' or query=='previous songs':# or query=='b':
            if flag_song==True:
                print("song changed")
                speak("song changed")
                previoussong()

        elif query=='pause song' or query=='pause' or query=='pass song' or query=='pass':# or query=='p':
            if flag_song==True:
                print("paused")
                speak("paused")
                pause()
                
        elif query=='unpause song' or query=='resume song' or query=='unpause' or query=='resume':# or query=='u':
            if flag_song==True:
                print("unpaused")
                speak("unpaused")
                unpause()

        elif query=='rise volume' or query=='rise sound' or query=='raise volume' or query=='raise sound':# or query=='r':
            if flag_song==True:
                rise_volume()

        elif query=='low volume':# or query=='l':
            if flag_song==True:
                low_volume()
                    
        elif query=='mute volume':# or query=='m':
            if flag_song==True:
                print("volume muted")
                speak("volume muted")
                mute()

        elif query=='maximum volume' or query=='max volume':# or query=='.':
            if flag_song==True:
                print("maximum volume set")
                speak("maximum volume set")
                max_volume()

        elif query=='middle volume' or query=='mid volume' or query=='normal volume':# or query==',':
            if flag_song==True:
                print("normal volume set")
                speak("normal volume set")
                mid_volume()

        elif query=='stop music' or query=='stop song' or query=='quit music' or query=='quit song' or query=='stop music player' or query=='stop player' or query=='quit music player' or query=='quit player':# or query == 'e':
            if flag_song==True:
                try:
                    mixer.music.stop()
                except:
                    pass
                music_player_quit()
                stopsong()
                flag_song=False
                flag_song_start=True
                print("player quited")
                speak("player quited")

        elif query=='restart music player':# or query=='x':
            if flag_song==True:
                try:
                    mixer.music.stop()
                except:
                    pass
                music_player_quit()
                stopsong()
                flag_song=False
                flag_song_start=True
                print("wait for few seconds")
                speak("wait for few seconds")
                time.sleep(1)
                if flag_song_start==True:
                    mid_volume()
                    if __name__ == '__main__':
                        Thread(target = music_player).start()
                    flag_song=True
                    flag_song_start=False

        elif query=='end':# or query=='h':
            try:
                mixer.music.stop()
                music_player_quit()
                stopsong()
            except:
                pass
            print("bye bye")
            speak("bye bye")
            break