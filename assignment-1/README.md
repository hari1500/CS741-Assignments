CS 741 Assignment-1 
XSS-Blocker  
Team:  
170050080: Chagam Dileep Kumar Reddy  
170050077: Nama N V S S HariKrishna  
170050070: Mohit Kumar Gupta  
170050093: Tarun Somavarapu  


# As of now, the extension can detect and block XSS whole script injections of the following types
## Input vectors with <script> tag 
        <script> alert(); </script>
        <  scRipT type="text/javascript">;</scriPt  >
## even when url with <script> tag encoded
        %3Cscript%3Ealert%28%29%3B%3C%2Fscript%3E

## inputs with onevent callbacks
        \<a onmouseover="alert(document.cookie)"\>\</a\>

## inputs which can call javascript functions
        <INPUT TYPE="IMAGE" SRC="javascript:alert('XSS');">


# AdBlocking
        all requests to urls containing words "googlead" , "pagead"  which provide adservices on learncbse.in are blocked to block the advertisements.
        

