<b><u>Sublime Text 3 Decipher Clips</u></b><br/>
==========================<br/>
<ul><b>Steps to Install:</b>
  <li>Clone repo or download and put it in your sublime Text 3/Packages folder.</li>
  <li>Windows 7 Default path:</li>
  <ul>
    <li>C:\Users\yourUserName\AppData\Roaming\Sublime Text 3\Packages</li>
  </ul>
  <li>Ubuntu Default path:</li>
  <ul>
    <li>~/.config/sublime-text-3</li>
  </ul>
</ul>

<i>Please note that for Windows 7, the “AppData” folder may be hidden. If you type “C:\Users\\\<yourUserName>\AppData\Roaming\Sublime Text 3\Packages”  into your Windows Explorer’s address bar you will be taken to that location.</i>

<b>How to call the clips/snippets:</b><br/>
Create a new XML document (The shortcuts for clips and snippets will only work with the XML extension). 

To use a clip, select text you want to wrap in tags and then either use the shortcut or context menu option.  

To use a snippet, type the snippet’s tab trigger and then hit tab. This will generate short fragments of text. 

Some snippets have placeholder fields. If your snippet has a placeholder field the cursor will move to that field automatically for you to update the text. If your snippets has multiple fields (such as the loop snippet) hitting tab will move the cursor to the next placeholder field. 

You can define your own keymappings in (Default (Linux or Windows).sublime-keymap)

To bring up the context menu, right click in the text editor. You can then navigate to the "Dec-Question Types" or "Dec-Question Elements" to view the avaliable clips. This will also display the current shortcuts for them. 

<b>Decipher Sublime Text 3 Clips Examples</b><br/>
=============================================<br/>

Code block selection short cuts:

ctrl+e = Select to the end of the current code block

example:
row1
row2
row2
row..
rowX

cursor at beginning or line row1 will select to the end of line rowX 
______________________________________________________________________

ctrl+a = Select to the beginning of the current code block
example:
Q1 this is a question
  <row label="r1">row1</row>
  <row label="r2">row2</row>
  <row label="r3">row2</row>
  <row label="r4">row...</row>
  <row label="r5">rowX</row>

cursor at end of line rowX will select to the beginning of Q1 line

________________________________


ctrl+shift+right = Select to the end of current line 
example:
Q1 this is a question
  <row label="r1">row1</row>
  <row label="r2">row2</row>
  <row label="r3">row2</row>
  <row label="r4">row...</row>
  <row label="r5">rowX</row>
cursor at beginning or line row1 will select to the end of line row1

_________________________________

ctrl+shift+down = Select to the beginning of the next cursor
example:
Q1 this is a question
  <row label="r1">row1</row>
  <row label="r2">row2</row>
  <row label="r3">row2</row>
  <row label="r4">row...</row>
  <row label="r5">rowX</row>
cursor at beginning or line row1 and second cursor at the beginning of rowX will select everything between two placed cursors

_________________________________



