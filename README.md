Decipher-subl
=======

create XML tags like NoteTab Pro (clips)

Ported most of Minh's clips

clone repo or download and put it in your sublime Text 2/Packages folder
Windows 7 Default path (C:\Users\yourUserName\AppData\Roaming\Sublime Text 2\Packages)
Ubuntu Default path (~/.config/sublime-text-2)

How to call the clips/snippets
You can define your own keymappings in (Default (Linux or Windows).sublime-keymap)
Right click context menu does provide the short cuts
Command Palette 

for python and JS syntax highlighting add this to your XML.tmLanguage
https://gist.github.com/krasserp/3de245d8f3d954303f0f
Windows 7 Default path (C:\Users\yourUserName\AppData\Roaming\Sublime Text 2\Packages\XML

Decipher Sublime Text 2 Clips

------------------------------


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


More soon...<br>
