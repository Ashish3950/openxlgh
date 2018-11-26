import win32clipboard
import time
from pynput import keyboard
while(1):
    try:
        copylist=[]
        copycomb = [ {keyboard.Key.ctrl_l,keyboard.KeyCode(char='c')},
                        {keyboard.Key.ctrl_l,keyboard.KeyCode(char='C')}]
        altcopy=[{keyboard.Key.alt_l,keyboard.KeyCode(char='z')},
                        {keyboard.Key.alt_l,keyboard.KeyCode(char='Z')}]
        altxcopy=[{keyboard.Key.alt_l,keyboard.KeyCode(char='x')},
                        {keyboard.Key.alt_l,keyboard.KeyCode(char='X')}]
        altxdel=[{keyboard.Key.alt_l,keyboard.KeyCode(char='d')},
                        {keyboard.Key.alt_l,keyboard.KeyCode(char='D')}]
        current= set()
        def on_press(key):
            if any ([key in combo for combo in (copycomb + altcopy +altxcopy+altxdel)]):
                current.add(key)
                if any (all (k in current for k in combo) for combo in altxdel):
                    while len(copylist) > 0 : copylist.pop() 
                    print('copylist is cleared')
                    current.discard(keyboard.KeyCode(char='d'))
                    current.discard(keyboard.KeyCode(char='D'))
                elif any (all (k in current for k in combo) for combo in altcopy):
                    win32clipboard.OpenClipboard()
                    if (len(copylist) not in [0,1]):
                        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                        if(data in copylist):
                            temp=copylist.index(data)
                        else:
                            copylist.insert(0,data)
                            temp=0   
                        if not ((temp+1)==len(copylist)):
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(copylist[temp+1])
                            current.discard(keyboard.KeyCode(char='z'))
                            current.discard(keyboard.KeyCode(char='Z'))
                            print("text is set to clipbord index +1")
                    win32clipboard.CloseClipboard()
                elif any (all (k in current for k in combo) for combo in altxcopy):
                    win32clipboard.OpenClipboard()
                    if (len(copylist) not in [0,1]):
                        data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                        if(data in copylist):
                            temp=copylist.index(data)
                        else:
                            copylist.insert(0,data)
                            temp=0   
                        if not ((temp==0)):
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardText(copylist[temp-1])
                            current.discard(keyboard.KeyCode(char='x'))
                            current.discard(keyboard.KeyCode(char='X'))
                            print("text is set to clipbord index -1")
                    win32clipboard.CloseClipboard()
                
                elif any (all (k in current for k in combo) for combo in copycomb):
                    time.sleep(0.5)
                    win32clipboard.OpenClipboard()
                    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                    win32clipboard.CloseClipboard()
                    if data:
                        if not (len(copylist)==0):
                            if not (data==copylist[0]):
                                copylist.insert(0,data)
                                current.discard(keyboard.KeyCode(char='c'))
                                current.discard(keyboard.KeyCode(char='C'))
                                print('data is inserted into list')
                        else:
                            copylist.insert(0,data)
                            current.discard(keyboard.KeyCode(char='c'))
                            current.discard(keyboard.KeyCode(char='C'))
                            print('data is inserted into list')
                
        def on_release(key):
            if any([key in combo for combo in copycomb]) and key in current:
                current.remove(key)
            elif any([key in combo for combo in altcopy]) and key in current:
                current.remove(key)
            elif any([key in combo for combo in altxcopy]) and key in current:
                current.remove(key)
        
        # Collect events until released
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
    
    except:
        pass
