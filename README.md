<b><u>Sublime Text 2 Decipher Clips</u></b><br/>
==========================<br/><br/>
<b>Steps to Install:</b><br/>
Clone repo or download and put it in your sublime Text 2/Packages folder.<br/>
Windows 7 Default path:<br/>
C:\Users\yourUserName\AppData\Roaming\Sublime Text 2\Packages<br/>
Ubuntu Default path:<br/>
~/.config/sublime-text-2

Please note that for Windows 7, the “AppData” folder may be hidden. If you type “C:\Users\<yourUserName>\AppData\Roaming\Sublime Text 2\Packages”  into your Windows Explorer’s address bar you will be taken to that location.


<b>How to call the clips/snippets:</b><br/>
Create a new XML document (The shortcuts for clips and snippets will only work with the XML extension). 

To use a clip, select text you want to wrap in tags and then either use the shortcut or context menu option.  

To use a snippet, type the snippet’s tab trigger and then hit tab. This will generate short fragments of text. 

Some snippets have placeholder fields. If your snippet has a placeholder field the cursor will move to that field automatically for you to update the text. If your snippets has multiple fields (such as the loop snippet) hitting tab will move the cursor to the next placeholder field. 

You can define your own keymappings in (Default (Linux or Windows).sublime-keymap)
Right click context menu does provide the short cuts
Command Palette 

For python and JS syntax highlighting add this to your XML.tmLanguage file
https://gist.github.com/krasserp/3de245d8f3d954303f0f<br/>
Windows 7 Default path (C:\Users\yourUserName\AppData\Roaming\Sublime Text 2\Packages\XML)

Decipher Sublime Text 2 Clips

------------------------------
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




Command: <b>MM::Html</b><br>
Makes an &lt;html&gt; tag in the survey and replaces blank lines with &lt;br/&gt; &lt;br/&gt;

Command: <b>MM::Strip</b><br>
Strips xml off of text. 

Command: <b>MM::Values</b><br>
Adds Values to rows/cols/choices based on the item label. If labels do not contain digits defaults to 1, 2, 3, etc

Command: <b>MM::Image Tags</b><br>
Inserts image name into an image tag. 

Example:<br>
Placeholder.jpg -&gt; &lt;img src="[rel Placeholder.jpg]" alt="Image" class="custImage" /&gt;

Command: <b>MM::Reverse Order</b><br>
Flips selected lines.

Command: <b>MM::Make DCM</b><br>
Experimental DCM maker<br>
Select your res tags and label each with a number. 

Example:<br>
[1]<br>
Res level 1<br>
Res level 2<br>

[2]<br>
Res level 1<br>
Res level 2 <br>
Res level 3<br>

You will be prompted to enter:<br>
QuestionLabel-Number of attributes-Columns desired in dcm-Tasks(loops)-Versions<br>
Q1-4-5-10-100

Command: <b>MM::Split Question</b><br>
Splits question based on the number of pages specified. 

Example:<br>
[5]<br>
&lt;radio label="Q1"&gt;<br>
&lt;title&gt;Some question text?&lt;/title&gt;<br>
&lt;comment&gt;Select one&lt;/comment&gt;<br>
  &lt;col label="c1"&gt;1&lt;/col&gt;<br>
  &lt;col label="c2"&gt;2&lt;/col&gt;<br>
  &lt;col label="c3"&gt;3&lt;/col&gt;<br>
  &lt;col label="c4"&gt;4&lt;/col&gt;<br>

  &lt;row label="r1"&gt;Row 1&lt;/row&gt;<br>
  &lt;row label="r2"&gt;Row 2&lt;/row&gt;<br>
  &lt;row label="r3"&gt;Row 3&lt;/row&gt;<br>
  &lt;row label="r4"&gt;Row 4&lt;/row&gt;<br>
  ...<br>

Command: <b>MM::Make SCols</b><br>
Column maker.

Command: <b>MM::Make list</b><br>
Makes an html list. Type of list can be specified with a [ol|ul]. Defaults to &lt;ul&gt; if neither is specified

Command: <b>MM::Clean</b><br>
Removes things in []'s or &lt;b&gt;[]&lt;/b&gt;'s<br>
Also fixes unicode character's and &'s

Command: <b>MM::No Answer</b><br>
Creates <noanswer> row.

Example:<br>
97 Don't know -> &lt;noanswer label="na97"&gt;Don't Know&lt;/noanswer&gt;<br>
or <br>
r97 Don't know -> &lt;noanswer label="na97"&gt;Don't Know&lt;/noanswer&gt;<br>

Command: <b>MM::AutoSum</b><br>
Little command that is coupled with a snippet I have. I will work on getting those uploaded eventually.

-----------------------
<h3>List of Snippets</h3>

|File Name|Short Cut|Description|
|:------------|:----------|:-----------|
|AnchorTag|anchor|Creates an anchor tag|
|Block|block|Creates a block tag|
|Breakx1|br1|Creates one br tag|
|Breakx2|br2|Creates two br tags|
|ColLegendRows|cl|Creates a colLegendRows attribute |
|Comment|com|Creates a comment tag|
|Condition|cond|Creates a condition attribute|
|Css|css|Creates a style tag for "respview.client.css"|
|Exclusive|ee|Creates two attributes: randomize="0" exclusive="1"|
|ExecBlock|exec|Creates an exec tag|
|Goto|goto|Creates a goto tag|
|Label|label|Creates a label tag|
|Loop|loop|Creates a loop tag wrapping a block tag|
|OpenEnd|oe|Creates three attributes: open="1" openSize="25" randomize="0"|
|PageHead|ph|Creates a style tag for "page.head"|
|PostText|post|Creates an attribute for posttext|
|QuestionAfter|qa|Creates a style tag for "question.after"|
|Quota|quota|Create a quota tag|
|Rating|rating|Creates two attributes: type="rating" values="order"|
|RemoveFromBase|rfb|Creates two attributes: aggregate="0" percentages="0"|
|ResTag|res|Creates a resource tag|
|Shuffle|sh|Creates the attribute: shuffle="rows"|
|States|states|Creates choices for all US states|
|Suspend|sus|Creates a suspend tag|
|Term|term|Creates a term tag|
|Validate|val|Creates a validate tag|
|VirtualBlock|virtual|Creates a virtual tag|
|WhereExecute|wex|Creates the attribute: where="execute"|
|WhereReport|wrp|Creates the attribute: where="report"|

<br/>