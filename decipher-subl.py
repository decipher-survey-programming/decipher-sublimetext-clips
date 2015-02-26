import sublime, sublime_plugin,re

#define survey context
def returnContext(self):
    returnString = self.view.find('surveyType=(.*)',0)
    if returnString:
        returnString = self.view.substr(returnString)
        return returnString[11:14]
    else:
        return ' '
# returns array [input, label,title]
def tidyQuestionInput(input):
    input = input.strip()
    input = re.sub(r"^(\w?\d+)\.(\d+)",r"\1_\2",input)

    while "\n\n" in input:
        input = input.replace("\n\n", "\n")

    label = re.split(r"^([a-zA-Z0-9-_]+)+(\.|:|\)|\s)", input, 1)[1]
    input = re.split(r"^([a-zA-Z0-9-_]+)+(\.|:|\)|\s)", input, 1)[-1]

    if label[0].isdigit():
        label = "Q" + label
    if "@" in input:
        title = input[0:(input.index("@"))]
    else:
        input_array = []
        if "<row" in input:
            input_array.append(input.index("<row"))
        if "<col" in input:
            input_array.append(input.index("<col"))
        if "<choice" in input:
            input_array.append(input.index("<choice"))
        if "<comment" in input:
            input_array.append(input.index("<comment"))
        if "<group" in input:
            input_array.append(input.index("<group"))
        if "<net" in input:
            input_array.append(input.index("<net"))
        if "<exec" in input:
            input_array.append(input.index("<exec"))
        if len(input_array) == 0:
            title = input
        else:
          input_index = min(input_array)
          title = input[0:input_index]


    input = input.replace(title, "")
    return [input, label, title]

def tidySurveyInput(input):
    input = input.encode()
    input = re.sub("\t+", " ", input)
    input = re.sub("\n +\n", "\n\n", input)
    funkyChars = [(chr(133),'...'),(chr(145),"'"),(chr(146),"'"),(chr(147),'"'),(chr(148),'"'),(chr(151),'--')]
    for pair in funkyChars:
        input = input.replace(pair[0],pair[1])
    input = re.sub("\n{3,}", "\n\n", input)
    input = input.replace("&", "&amp;")
    input = input.replace("&amp;#", "&#")
    return input
# normal survey return array header & footer
def newSurvey():
    HEADER = """<survey name="Survey"
                 alt=""
                 autosave="0"
                 extraVariables="source,list,url,record,ipAddress,userAgent,decLang"
                 compat="127"
                 builderCompatible="1"
                 secure="0"
                 setup="time,term,quota,decLang"
                 ss:disableBackButton="1"
                 mobile="compat"
                 mobileDevices="smartphone,tablet,featurephone,desktop"
                 state="testing">

                <samplesources default="0">
                  <samplesource list="0" title="default">
                    <exit cond="qualified"><b>Thanks again for completing the survey!<br/><br/>Your feedback and quick response to this survey are greatly appreciated.</b></exit>
                    <exit cond="terminated"><b>Thank you for your input!</b></exit>
                    <exit cond="overquota"><b>Thank you for your input!</b></exit>
                  </samplesource>
                </samplesources>"""
    FOOTER = """<marker name="qualified"/></survey>"""

    return[HEADER,FOOTER]

def newSurveyCMB():
    HEADER = """
            <survey
             name="Survey"
             alt=""
             autosave="1"
             extraVariables="source,list,url,record,ipAddress,userAgent,decLang"
             compat="125"
             builderCompatible="1"
             secure="0"
             setup="time,term,quota,decLang"
             ss:disableBackButton="1"
             trackCheckbox="1"
             mobile="compat"
             mobileDevices="smartphone,tablet,featurephone,desktop"
             state="testing"
             unique="">

            <!-- IMPORTANT: Remember to copy the nstyles file from v2/cmb/temp-cmb to the current project directory -->

            <samplesources default="0">
              <samplesource list="0" title="default">
                <exit cond="qualified"><b>Thanks again for completing the survey!<br/><br/>Your feedback and quick response to this survey are greatly appreciated.</b></exit>
                <exit cond="terminated"><b>Thank you for your input!</b></exit>
                <exit cond="overquota"><b>Thank you for your input!</b></exit>
              </samplesource>
            </samplesources>"""
    FOOTER = """<marker name="qualified"/></survey>"""
    return[HEADER,FOOTER]

def newSurveyEBAY():
    HEADER = """<survey
             name="eBay Survey"
             alt=""
             autosave="1"
             extraVariables="source,list,url,record,ipAddress,userAgent,co,decLang"
             compat="125"
             builderCompatible="1"
             secure="0"
             state="testing"
             setup="time,term,quota,decLang"
             ss:disableBackButton="1"
             displayOnError="all"
             unique=""
             mobile="compat"
             mobileDevices="smartphone,tablet,featurephone,desktop"
             lang="english"
             otherLanguages="danish,german,finnish,french,norwegian,spanish,swedish,uk">

            <res label="privacyText">Privacy Policy</res>
            <res label="helpText">Help</res>

            <!-- Remove or add countries as needed -->
            <languages default="english">
              <language name="danish" var="co" value="dk"/>
              <language name="german" var="co" value="de"/>
              <language name="finnish" var="co" value="fi"/>
              <language name="french" var="co" value="fr"/>
              <language name="norwegian" var="co" value="no"/>
              <language name="spanish" var="co" value="es"/>
              <language name="swedish" var="co" value="se"/>
              <language name="uk" var="co" value="uk"/>
              <language name="english" var="co" value="us"/>
            </languages>

            <!-- Remove or add countries as needed -->
            <radio label="vco" title="Country" virtual="bucketize(co)">
              <row label="dk">Denmark</row>
              <row label="de">Germany</row>
              <row label="fi">Finland</row>
              <row label="fr">France</row>
              <row label="no">Norway</row>
              <row label="es">Spain</row>
              <row label="se">Sweden</row>
              <row label="uk">United Kingdom</row>
              <row label="us">United Sates</row>
            </radio>

            <!-- Remove or add countries as needed -->
            <samplesources default="1">
              <samplesource list="1" title="eBay Sample">
             <!--  <var name="source" filename="invited.txt" unique="1"/>  un-comment this before launching -->
               <var name="co" required="1" values="dk,de,fi,fr,no,es,se,uk,us"/>
                <exit cond="qualified and co=='dk'" timeout="8" url="http://www.ebay.dk">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='dk'" timeout="8" url="http://www.ebay.dk">Thank you for your input!</exit>
                <exit cond="overquota and co=='dk'" timeout="8" url="http://www.ebay.dk">Thank you for your input!</exit>

                <exit cond="qualified and co=='de'" timeout="8" url="http://www.ebay.de">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='de'" timeout="8" url="http://www.ebay.de">Thank you for your input!</exit>
                <exit cond="overquota and co=='de'" timeout="8" url="http://www.ebay.de">Thank you for your input!</exit>

                <exit cond="qualified and co=='fi'" timeout="8" url="http://www.ebay.fi">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='fi'" timeout="8" url="http://www.ebay.fi">Thank you for your input!</exit>
                <exit cond="overquota and co=='fi'" timeout="8" url="http://www.ebay.fi">Thank you for your input!</exit>

                <exit cond="qualified and co=='fr'" timeout="8" url="http://www.ebay.fr">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='fr'" timeout="8" url="http://www.ebay.fr">Thank you for your input!</exit>
                <exit cond="overquota and co=='fr'" timeout="8" url="http://www.ebay.fr">Thank you for your input!</exit>

                <exit cond="qualified and co=='no'" timeout="8" url="http://www.ebay.no">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='no'" timeout="8" url="http://www.ebay.no">Thank you for your input!</exit>
                <exit cond="overquota and co=='no'" timeout="8" url="http://www.ebay.no">Thank you for your input!</exit>

                <exit cond="qualified and co=='es'" timeout="8" url="http://www.ebay.es">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='es'" timeout="8" url="http://www.ebay.es">Thank you for your input!</exit>
                <exit cond="overquota and co=='es'" timeout="8" url="http://www.ebay.es">Thank you for your input!</exit>

                <exit cond="qualified and co=='se'" timeout="8" url="http://www.ebay.se">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='se'" timeout="8" url="http://www.ebay.se">Thank you for your input!</exit>
                <exit cond="overquota and co=='se'" timeout="8" url="http://www.ebay.se">Thank you for your input!</exit>

                <exit cond="qualified and co=='uk'" timeout="8" url="http://www.ebay.co.uk">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='uk'" timeout="8" url="http://www.ebay.co.uk">Thank you for your input!</exit>
                <exit cond="overquota and co=='uk'" timeout="8" url="http://www.ebay.co.uk">Thank you for your input!</exit>

                <exit cond="qualified and co=='us'" timeout="8" url="http://www.ebay.com">Survey Completed - Thank you for your time and opinions!</exit>
                <exit cond="terminated and co=='us'" timeout="8" url="http://www.ebay.com">Thank you for your input!</exit>
                <exit cond="overquota and co=='us'" timeout="8" url="http://www.ebay.com">Thank you for your input!</exit>
              </samplesource>
            </samplesources>


            <html label="StandardIntro" where="survey">Thank you for taking the time to complete this survey. Your opinions are extremely valuable, and will help us to improve your eBay experience. Your responses are completely confidential and will only be used for research purposes. Your responses will be analyzed only in combination with those of other participants. See our <a href="http://pages.ebay.com/help/policies/privacy-policy.html" target="_blank">privacy policy</a>.</html>
            <suspend/>

            """


    FOOTER = """<marker name="qualified"/></survey>"""
    return[HEADER,FOOTER]

def newSurveyFMA():
    HEADER = """<survey
             name="Survey"
             alt=""
             autosave="0"
             extraVariables="source,list,url,record,ipAddress,userAgent,decLang"
             compat="124"
             builderCompatible="1"
             secure="0"
             state="testing"
             setup="time,term,quota,decLang"
             ss:disableBackButton="1"
             fwoe="text"
             mobile="compat"
             mobileDevices="smartphone,tablet,featurephone,desktop"
             ss:logoFile="fma/surveysonline_logo.gif"
             ss:logoPosition="left">

            <samplesources default="0">
              <samplesource list="0" title="default">
                <exit cond="qualified"><b>Thanks again for completing the survey!<br/><br/>Your feedback and quick response to this survey are greatly appreciated.</b></exit>
                <exit cond="terminated"><b>Thank you for your input!</b></exit>
                <exit cond="overquota"><b>Thank you for your input!</b></exit>
              </samplesource>
            </samplesources>"""

    FOOTER = """<marker name="qualified"/>

                <radio label="vStatus" title="Status">
                <virtual>
                if 'recovered' in markers:
                    data[0][0] = 3
                else:
                    if 'qualified' in markers:
                        data[0][0] = 2
                    elif 'OQ' in markers:
                        data[0][0] = 1
                    else:
                        data[0][0] = 0
                </virtual>
                  <row label="r1">Term</row>
                  <row label="r2">OQ</row>
                  <row label="r3">Quals</row>
                  <row label="r4">Partials</row>
                </radio>

                </survey>"""
    return[HEADER,FOOTER]

def newSurveyGDI():
    HEADER = """<survey
                 name="Survey"
                 alt=""
                 autosave="0"
                 extraVariables="source,list,url,record,ipAddress,userAgent,decLang"
                 compat="125"
                 builderCompatible="1"
                 secure="0"
                 state="testing"
                 setup="time,term,quota,decLang"
                 ss:disableBackButton="1"
                 fixedWidth="tight"
                 mobile="compat"
                 mobileDevices="smartphone,tablet,featurephone,desktop"
                 zeroPad="1">

                <samplesources default="1">
                  <samplesource list="1" title="Greenfield/Toluna">
                    <var name="gid" unique="1"/>
                    <exit cond="qualified" url="http://ups.surveyrouter.com/soqualified.aspx?gid=${gid}"/>
                    <exit cond="terminated" url="http://ups.surveyrouter.com/soterminated.aspx?gid=${gid}"/>
                    <exit cond="overquota" url="http://ups.surveyrouter.com/soquotafull.aspx?gid=${gid}"/>
                  </samplesource>
                </samplesources>

                <number altlabel="record" fwidth="10" label="vrec" size="10" title="Record As Number" virtual="if record:  data[0][0] = int(record)"/>
                """

    FOOTER = """<marker name="qualified"/></survey>"""
    return[HEADER,FOOTER]

def newSurveySRG():
    HEADER = """<survey
             name="Survey"
             alt=""
             autosave="0"
             extraVariables="source,list,url,record,ipAddress,userAgent,flashDetected,decLang"
             compat="125"
             builderCompatible="1"
             secure="0"
             state="testing"
             setup="time,term,quota,decLang"
             mobile="compat"
             mobileDevices="smartphone,tablet,featurephone,desktop"
             ss:disableBackButton="1"
             ss:colorScheme="theme_red-01"
             fixedWidth="tight">

            <samplesources default="0">
              <samplesource list="0" title="default">
                <exit cond="qualified"><b>Thanks again for completing the survey!<br/><br/>Your feedback and quick response to this survey are greatly appreciated.</b></exit>
                <exit cond="terminated"><b>Thank you for your input!</b></exit>
                <exit cond="overquota"><b>Thank you for your input!</b></exit>
              </samplesource>
            </samplesources>"""
    FOOTER = """<marker name="qualified"/></survey>"""
    return[HEADER,FOOTER]

def newSurveyGMI():
    HEADER = """<survey
             name="Survey"
             alt=""
             autosave="1"
             autosaveKey="ac"
             extraVariables="source,list,url,record,ipAddress,userAgent,flashDetected,ac,sn,lang,co,decLang"
             setup="time,term,quota,decLang"
             ss:disableBackButton="1"
             displayOnError="all"
             unique=""
             compat="125"
             builderCompatible="1"
             secure="0"
             mobile="compat"
             mobileDevices="smartphone,tablet,featurephone,desktop"
             state="testing">

            <exec when="init">
            db_completed = Database( name="completed" )
            </exec>
            <exec>
            db_id = ac
            p.completedID = db_id
            </exec>

            <samplesources default="1">
              <completed>It seems you have already entered this survey.</completed>
              <invalid>You are missing information in the URL. Please verify the URL with the original invite.</invalid>
              <samplesource list="1" title="GMI">
                <var name="ac" unique="1"/>
                <var name="sn" required="1"/>
                <var name="lang" required="1"/>
                <exit cond="qualified" url="http://globaltestmarket.com/20/survey/finished.phtml?ac=${ac}&amp;sn=${sn}&amp;lang=${lang}"/>
                <exit cond="terminated" url="http://globaltestmarket.com/20/survey/finished.phtml?ac=${ac}&amp;sn=${sn}&amp;lang=${lang}&amp;sco=s"/>
                <exit cond="overquota" url="http://globaltestmarket.com/20/survey/finished.phtml?ac=${ac}&amp;sn=${sn}&amp;lang=${lang}&amp;sco=o"/>
              </samplesource>
            <samplesources>

            <html cond="db_completed.has(p.completedID)" final="1" label="dupe" where="survey">It seems you have already participated in this survey.</html>
            """
    FOOTER = """<marker name="qualified"/>
                <exec when="finished">
                if gv.survey and gv.survey.root.state.live:
                    db_completed.add(p.completedID)
                </exec>

                </survey>"""
    return[HEADER,FOOTER]

def fixUniCode(input):
    input = input.replace(u"\u2019", "'").replace(u"\u2018", "'").replace(u"\u201C", "\"").replace(u"\u201D", "\"")
    input = re.sub('&\s', '&amp; ',input)
    return input


#need to find a better solution for the surveyType set up
class setSurveyType(sublime_plugin.TextCommand):
    def run(self, edit):
        sels = self.view.sel()
        sel = sels[0]
        surveyType = "<!-- surveyType="+self.view.substr(sel)+" -->"
        self.view.replace(edit,sel, surveyType)

################# Survey types

class makeSurveyCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel).strip()
                input = tidySurveyInput(input)
                #print input
                headerFooter =[]
                ### different variables dependant on survey type
                
                if docType =='CMB':
                    headerFooter = newSurveyCMB()
                    printPage = "%s\n\n%s\n\n%s" % (headerFooter[0], input, headerFooter[1])
                    
                    headerFooter =[]
                elif docType =='EBA':
                    print 'ebay found'
                    headerFooter = newSurveyEBAY()
                    printPage = "%s\n\n%s\n\n%s" % (headerFooter[0], input, headerFooter[1])
                    print headerFooter
                    headerFooter =[]
                elif docType =='FMA':
                    headerFooter = newSurveyFMA()
                    print headerFooter
                    printPage = "%s\n\n%s\n\n%s" % (headerFooter[0], input, headerFooter[1])
                    headerFooter =[]
                elif docType =='GDI':
                    headerFooter = newSurveyGDI()
                    printPage = "%s\n\n%s\n\n%s" % (headerFooter[0], input, headerFooter[1])
                    headerFooter =[]
                elif docType =='SRG':
                    headerFooter = newSurveySRG()
                    printPage = "%s\n\n%s\n\n%s" % (headerFooter[0], input, headerFooter[1])
                    headerFooter =[]
                elif docType =='GMI':
                    headerFooter = newSurveyGMI()
                    printPage = "%s\n\n%s\n\n%s" % (headerFooter[0], input, headerFooter[1])
                    headerFooter =[]
                else:
                    headerFooter = newSurvey()
                    print 'in else somehow'
                    printPage = "%s\n\n%s\n\n%s" % (headerFooter[0], input, headerFooter[1])
                    headerFooter =[]

                #print headerFooter
                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print 'could not create survey layout'
            print e

################# Question types
class makeRadioCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                inputLabelTitle = tidyQuestionInput(input)
                input = inputLabelTitle[0]
                label = inputLabelTitle[1]
                title = inputLabelTitle[2]

                if docType == 'CMB':
                    colCount = len(input.split("<col"))-1

                output = input
                #test for and adjust comment for 2d question
                if "<comment>" not in input:
                    if ("<row" in output) and ("<col" in output):
                        comment = "<comment>Select one in each row</comment>\n" if docType != 'SRG' else  "<comment>Please select one in each row</comment>\n"
                    else:
                        comment = "<comment>Select one</comment>\n" if docType != 'SRG' else "<comment>Please select one</comment>\n"

                # compose our new radio question
                if docType == 'FMA':
                    printPage = "<radio label=\"%s\">\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), title.strip(), output)
                elif docType == 'HAP':

                    rowlegend = ""

                    if ("<row" in output) and not ("<col" in output):
                        rowlegend=' rowLegend=\"right\"'
                        print 'add row legend!!!!!!'
                    # compose our new radio question
                    if "<comment>" not in input:
                      printPage = "<radio label=\"%s\"%s>\n  <title>%s</title>\n  %s  %s\n</radio>\n<suspend/>" % (label.strip(), rowlegend, title.strip(), comment, output)
                    else:
                      printPage = "<radio label=\"%s\"%s>\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), rowlegend, title.strip(), output)
                elif docType == 'CMB':
                        if (("<row" in output) and ("<col" in output) and (colCount > 1)) or not ("<row" in output):
                            style = ''
                        else:
                            style = ' style=\"noGrid\" ss:questionClassNames=\"flexGrid\"'

                        # compose our new radio question
                        if "<comment>" not in input:
                          printPage = "<radio label=\"%s\"%s>\n  <title>%s</title>\n  %s  %s\n</radio>\n<suspend/>" % (label.strip(), style, title.strip(), comment, output)
                        else:
                          printPage = "<radio label=\"%s\"%s>\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), style, title.strip(), output)

                else:
                    if "<comment>" not in input:
                      printPage = "<radio label=\"%s\">\n  <title>%s</title>\n  %s  %s\n</radio>\n<suspend/>" % (label.strip(), title.strip(), comment, output)
                    else:
                      printPage = "<radio label=\"%s\">\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), title.strip(), output)


                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print "makeRadio clip failed:"
            print e

class makeRatingCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                inputLabelTitle = tidyQuestionInput(input)
                input = inputLabelTitle[0]
                label = inputLabelTitle[1]
                title = inputLabelTitle[2]

                if docType == 'CMB':
                    rowCount = len(input.split("<row"))-1
                    colCount = len(input.split("<col"))-1

                output = input
                shffl = ""
                style = ""
                comment = ''
                if docType == 'FMA':
                    printPage = "<radio label=\"%s%s%s\" type=\"rating\">\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), shffl, style, title.strip(), output)

                elif docType == 'HAP':
                    #DETERMINE IF WE NEED A 1D OR 2D COMMENT, SHUFFLE 2D ROWS OR COLS, ADD AVERAGES attribute.
                    if ("<row" in output) and ("<col" in output):
                        comment = "<comment>Select one in each row</comment>\n"
                        s = output.split("    ")
                        for x in s:
                            if x.count("value=") > 0:
                                if x.count("<col") > 0:
                                    shffl = " shuffle=\"rows\""
                                elif x.count("<row") > 0:
                                    shffl = " shuffle=\"cols\""
                    else:
                        comment = "<comment>Select one</comment>\n"

                    rowlegend=""

                    if ("<row" in output) and not ("<col" in output):
                        rowlegend=' rowLegend=\"right\"'

                    if "<comment>" not in input:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\"%s>\n  <title>%s</title>\n  %s  %s\n</radio>\n<suspend/>" % (label.strip(), rowlegend, shffl, style, title.strip(), comment, output)
                    else:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\"%s>\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), rowlegend, shffl, style, title.strip(), output)

                elif docType == 'CMB':

                    if ("<row" in output) and ("<col" in output):
                        comment = "<comment>Select one in each row</comment>\n"
                        s = output.split("    ")
                        for x in s:
                            if x.count("value=") > 0:
                                if x.count("<col") > 0:
                                    shffl = " shuffle=\"rows\""
                                elif x.count("<row") > 0:
                                    shffl = " shuffle=\"cols\""
                    else:
                        comment = "<comment>Select one</comment>\n"

                    if (("<row" in output) and ("<col" in output) and (colCount > 1)) or not ("<row" in output):
                        style = ''
                    else:
                        style = ' style=\"noGrid\" ss:questionClassNames=\"flexGrid\"'

                    if "<comment>" not in input:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\">\n  <title>%s</title>\n  %s  %s\n</radio>\n<suspend/>" % (label.strip(), shffl, style, title.strip(), comment, output)
                    else:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\">\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), shffl, style, title.strip(), output)
                elif docType == 'SRG':

                    if (("row" in output) or ("rows" in output)) and (("col" in output) or ("cols" in output)):
                        comment = "<comment>Please select one in each row</comment>\n"
                        s = output.split("    ")
                        for x in s:
                            if x.count("value=") > 0:
                                if x.count("<col") > 0:
                                    shffl = " shuffle=\"rows\""
                                elif x.count("<row") > 0:
                                    shffl = " shuffle=\"cols\""
                    else:
                        comment = "<comment>Please select one</comment>\n"

                    if "<comment>" not in input:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\">\n  <title>%s</title>\n  %s  %s\n</radio>\n<suspend/>" % (label.strip(), shffl, style, title.strip(), comment, output)
                    else:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\">\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), shffl, style, title.strip(), output)


                else:
                    #DETERMINE IF WE NEED A 1D OR 2D COMMENT, SHUFFLE 2D ROWS OR COLS, ADD AVERAGES attribute.
                    if (("row" in output) or ("rows" in output)) and (("col" in output) or ("cols" in output)):
                        comment = "<comment>Select one in each row</comment>\n"
                        s = output.split("    ")
                        for x in s:
                            if x.count("value=") > 0:
                                if x.count("<col") > 0:
                                    shffl = " shuffle=\"rows\""
                                elif x.count("<row") > 0:
                                    shffl = " shuffle=\"cols\""
                    else:
                        comment = "<comment>Select one</comment>\n"

                    if "<comment>" not in input:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\">\n  <title>%s</title>\n  %s  %s\n</radio>\n<suspend/>" % (label.strip(), shffl, style, title.strip(), comment, output)
                    else:
                        printPage = "<radio label=\"%s\"%s%s type=\"rating\">\n  <title>%s</title>\n  %s\n</radio>\n<suspend/>" % (label.strip(), shffl, style, title.strip(), output)


                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print "makeRating clip failed:"
            print e

class makeCheckboxCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                inputLabelTitle = tidyQuestionInput(input)
                input = inputLabelTitle[0]
                label = inputLabelTitle[1]
                title = inputLabelTitle[2]    

                
                #checkbox specific
                rowCount = len(input.split("<row"))-1
                colCount = len(input.split("<col"))-1
                comment = ''
                # add the all important line breakage
                output2 = input

                inputSpl = output2.split('\n')
                output2 = []

                nota_array = [">None of the above",">None of these",">None of the Above",">None of These"]
                noAns = "<noanswer"
                for x in inputSpl:
                    output = ""
                    for nota in nota_array:
                        print x
                        if nota in x and noAns not in x:
                            repwith = " exclusive=\"1\" randomize=\"0\"" + nota
                            output = x.replace(nota,repwith)

                    if output:
                        output2.append(output)
                    else:
                        output2.append(x)

                output = "\n".join(output2)
                if docType == 'CMB':
                    # set the appropriate comment
                    comment = "<comment>Select all that apply</comment>\n"

                    if ("<row" in output) and ("<col" in output) and (colCount > 1):
                        style = ''
                    else:
                        style = ' style=\"noGrid\" ss:questionClassNames=\"flexGrid\"'

                    # compose the question
                    if "<comment>" not in input:
                        printPage = "<checkbox label=\"%s\"%s atleast=\"1\">\n  <title>%s</title>\n  %s  %s\n</checkbox>\n<suspend/>" % (label.strip(), style, title.strip(), comment, output)
                    else:
                        printPage = "<checkbox label=\"%s\"%s atleast=\"1\">\n  <title>%s</title>\n  %s\n</checkbox>\n<suspend/>" % (label.strip(), style, title.strip(), output)

                elif docType =='HAP':
                    comment = "<comment>Select all that apply</comment>\n"
                    rowlegend=""

                    if ("<row" in output) and not ("<col" in output):
                        rowlegend =' rowLegend=\"right\"'
                        # compose the question
                    if "<comment>" not in input:
                            printPage = "<checkbox label=\"%s\" atleast=\"1\"%s>\n  <title>%s</title>\n  %s  %s\n</checkbox>\n<suspend/>" % (label.strip(), rowlegend, title.strip(), comment, output)
                    else:
                            printPage = "<checkbox label=\"%s\" atleast=\"1\"%s>\n  <title>%s</title>\n  %s\n</checkbox>\n<suspend/>" % (label.strip(), rowlegend, title.strip(), output)


                elif docType =='FMA':
                    # compose the question
                    printPage = "<checkbox label=\"%s\" atleast=\"1\">\n  <title>%s</title>\n  %s\n</checkbox>\n<suspend/>" % (label.strip(), title.strip(), output)
                elif docType =='SRG':
                        comment = "<comment>Please select all that apply</comment>\n"
                        # compose the question
                        if "<comment>" not in input:
                            printPage = "<checkbox label=\"%s\" atleast=\"1\">\n  <title>%s</title>\n  %s  %s\n</checkbox>\n<suspend/>" % (label.strip(), title.strip(), comment, output)
                        else:
                            printPage = "<checkbox label=\"%s\" atleast=\"1\">\n  <title>%s</title>\n  %s\n</checkbox>\n<suspend/>" % (label.strip(), title.strip(), output)
                else:
                        # set the appropriate comment
                    comment = "<comment>Select all that apply</comment>\n"
                    # compose the question
                    if "<comment>" not in input:
                        printPage = "<checkbox label=\"%s\" atleast=\"1\">\n  <title>%s</title>\n  %s  %s\n</checkbox>\n<suspend/>" % (label.strip(), title.strip(), comment, output)
                    else:
                        printPage = "<checkbox label=\"%s\" atleast=\"1\">\n  <title>%s</title>\n  %s\n</checkbox>\n<suspend/>" % (label.strip(), title.strip(), output)
                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeSelectCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                inputLabelTitle = tidyQuestionInput(input)
                input = inputLabelTitle[0]
                label = inputLabelTitle[1]
                title = inputLabelTitle[2]
                #start from output = to fill this class
                output = "\n  " + input

                # compose the select question
                printPage = "<select label=\"%s\" optional=\"0\">\n  <title>%s</title>  %s\n</select>\n<suspend/>" % (label.strip(), title.strip(), output)

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeTextareaCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                inputLabelTitle = tidyQuestionInput(input)
                input = inputLabelTitle[0]
                label = inputLabelTitle[1]
                title = inputLabelTitle[2]
                #start from output = to fill this class
                output = input
                if output != "":
                  output = "  " + output + "\n"

                if docType == 'FMA':
                       printPage = "<textarea label=\"%s\" optional=\"0\">\n  <title>%s</title>\n%s</textarea>\n<suspend/>" % (label.strip(), title.strip(), output)
                else :

                    #COMPOSE OUR QUESTION
                    if "<comment>" not in input:
                        comment = "<comment>Please be as specific as possible</comment>"
                        printPage = "<textarea label=\"%s\" optional=\"0\">\n  <title>%s</title>\n  %s\n%s</textarea>\n<suspend/>" % (label.strip(), title.strip(), comment, output)
                    else:
                        printPage = "<textarea label=\"%s\" optional=\"0\">\n  <title>%s</title>\n%s</textarea>\n<suspend/>" % (label.strip(), title.strip(), output)

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print "makeTextarea failed"
            print e

class makeTextCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                inputLabelTitle = tidyQuestionInput(input)
                input = inputLabelTitle[0]
                label = inputLabelTitle[1]
                title = inputLabelTitle[2]

                rowCount = len(input.split("<row"))-1
                colCount = len(input.split("<col"))-1
                #start from output = to fill this class
                # add the all important line breakage
                output = input
                if output != "":
                  output = "  " + output + "\n"

                if docType =='CMB':
                        if (("<row" in output) and ("<col" in output) and (colCount > 1)) or not ("<row" in output):
                            style = ''
                        else:
                            style = ' style=\"noGrid\"'
                        #COMPOSE OUR QUESTION
                        if "<comment>" not in input:
                            comment = "<comment>Please be as specific as possible</comment>\n"
                            printPage = "<text label=\"%s\" size=\"40\" optional=\"0\"%s>\n  <title>%s</title>\n  %s  %s\n</text>\n<suspend/>" % (label.strip(), style, title.strip(), comment, output)
                        else:
                            printPage = "<text label=\"%s\" size=\"40\" optional=\"0\"%s>\n  <title>%s</title>\n  %s\n</text>\n<suspend/>" % (label.strip(), style, title.strip(), output)

                elif docType =='FMA':
                    printPage = "<text label=\"%s\" size=\"40\" optional=\"0\">\n  <title>%s</title>\n%s</text>\n<suspend/>" % (label.strip(), title.strip(), output)

                else:
                    if "<comment>" not in input:
                        comment = "<comment>Please be as specific as possible</comment>"
                        printPage = "<text label=\"%s\" size=\"40\" optional=\"0\">\n  <title>%s</title>\n  %s\n%s</text>\n<suspend/>" % (label.strip(), title.strip(), comment, output)
                    else:
                        printPage = "<text label=\"%s\" size=\"40\" optional=\"0\">\n  <title>%s</title>\n%s</text>\n<suspend/>" % (label.strip(), title.strip(), output)


                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeNumberCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                inputLabelTitle = tidyQuestionInput(input)
                input = inputLabelTitle[0]
                label = inputLabelTitle[1]
                title = inputLabelTitle[2]
                #start from output = to fill this class
                                    # add the all important line breakage
                output = input
                if output != "":
                    output = "  " + output + "\n"
                if docType =='FMA':
                    printPage = "<number label=\"%s\" size=\"3\" optional=\"0\">\n  <title>%s</title>\n%s</number>\n<suspend/>" % (label.strip(), title.strip(), output)

                else:
                    #COMPOSE OUR QUESTION
                    if "<comment>" not in input:
                        comment = "<comment>Please enter a whole number</comment>\n"
                        printPage = "<number label=\"%s\" size=\"3\" optional=\"0\">\n  <title>%s</title>\n  %s%s</number>\n<suspend/>" % (label.strip(), title.strip(), comment, output)
                    else:
                        printPage = "<number label=\"%s\" size=\"3\" optional=\"0\">\n  <title>%s</title>\n%s</number>\n<suspend/>" % (label.strip(), title.strip(), output)
                
                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makePipeCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            #docType =  returnContext(self)
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                 # get rid of blank lines
                while "\n\n" in input:
                    input = input.replace("\n\n", "\n")

                output = input

                # compose our new pipe tag
                printPage = "<pipe label=\"\" capture=\"\">\n  %s\n</pipe>\n" % (output)

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print 'make pipe failed'
            print e
############# QUESTION ELEMENTS ######################
class makeRowCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            for sel in sels:
                count = 0
                printPage = ''
                extra = ''
                input = self.view.substr(sel)
                #CLEAN UP THE TABS
                input = re.sub("\t+", " ", input)

                #CLEAN UP SPACES
                input = re.sub("\n +\n", "\n\n", input)

                #CLEAN UP THE EXTRA LINE BREAKS
                input = re.sub("\n{2,}", "\n", input)
                input = fixUniCode(input)

                input = input.strip().split("\n")
                #ebay has a different openSize
                openSize =  '45' if docType =='EBA' else '25'

                for x in range(0,len(input)):
                    input[x] = re.sub("^[a-zA-Z0-9]{1,2}[\.:\)][ \t]+", "", input[x])

                for x in input:

                    if "other" in input[count].strip().lower() and "specify" in input[count].strip().lower():
                      input[count] = input[count].strip().replace("_", "")
                      extra=' open=\"1\" openSize=\"'+openSize+'\" randomize=\"0\"'
                    else:
                      extra = ''
                    printPage += "  <row label=\"r%s\"%s>%s</row>\n" % (str(count+1), extra, input[count].strip())
                    count += 1
                # thanks to replace the regions keep updated with their start and end point
                self.view.replace(edit,sel, printPage)

        except Exception, e:
            print e



class makeRowrCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        try:
            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            for sel in sels:
                printPage = ''
                extra = ''
                input = self.view.substr(sel)
                #CLEAN UP THE TABS
                input = re.sub("\t+", " ", input)

                #CLEAN UP SPACES
                input = re.sub("\n +\n", "\n\n", input)

                #CLEAN UP THE EXTRA LINE BREAKS
                input = re.sub("\n{2,}", "\n", input)
                input = fixUniCode(input)

                input = input.strip().split("\n")
                #ebay has a different openSize
                openSize =  '45' if docType =='EBA' else '25'
                counter = 0
                count = len(input)

                for x in range(0,len(input)):
                    input[x] = re.sub("^[a-zA-Z0-9]{1,2}[\.:\)][ \t]+", "", input[x])

                for x in input:
                    
                    if "other" in input[count-1].strip().lower() and "specify" in input[count-1].strip().lower():
                      input[count-1] = input[count-1].replace("_", "")
                      extra=' open=\"1\" openSize=\"'+openSize+'\" randomize=\"0\"'
                    else:
                      extra = ''
                    printPage += "  <row label=\"r%s\"%s>%s</row>\n" % (str(count), extra, input[counter].strip())
                    count -= 1
                    counter +=1
                # thanks to replace the regions keep updated with their start and end point
                self.view.replace(edit,sel, printPage)

        except Exception, e:
            print e


class makeRowsMatchLabelCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel).strip()
                input = fixUniCode(input)
                #SPLIT UP INTO ROWS
                input = input.split("\n")
                #ebay has a different openSize
                openSize =  '45' if docType =='EBA' else '25'
                #ITERATE ROWS
                count = 0
                for line in input:
                     line = line.strip()
                     print line
                     #SPLIT ON WHITESPACE -- REMOVE LEADING AND TRAILING WS
                     parts = re.split(r"\s",line,1) 

                     #GET RID OF EXTRA SPACES
                     ordinal= parts[0].strip()
                     ordinal= ordinal.rstrip('.')
                     ordinal= ordinal.rstrip(')')

                     #GET RID OF EXTRA SPACES
                     if len(parts) == 2:
                       content = parts[1].strip()


                     extra=""

                     if "other" in content.lower() and "specify" in content.lower():
                       content = content.replace("_", "")
                       extra=' open=\"1\" openSize=\"'+openSize+'\" randomize=\"0\"'

                     #COMPOSE ROW
                     if ordinal[0].isalpha() and (len(parts) == 2):
                       printPage += "  <row label=\"%s\"%s>%s</row>\n" % (ordinal, extra, content)
                     elif ordinal[0].isdigit():
                       printPage += "  <row label=\"r%s\"%s>%s</row>\n" % (ordinal, extra, content)
                     elif (len(parts) == 2):
                       printPage += "  <row label=\"%s\"%s>%s</row>\n" % (ordinal, extra, content)
                     else:
                       count += 1
                       printPage += "  <row label=\"r%s\"%s>%s</row>\n" % (str(count), extra, line)

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeRowsMatchValuesCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                input = fixUniCode(input)
                #SPLIT UP INTO ROWS
                input = input.split("\n")
                #ebay has a different openSize
                openSize =  '45' if docType =='EBA' else '25'
                #ITERATE ROWS
                for line in input:
                    line = line.strip()
                    print line
                    #SPLIT ON WHITESPACE -- REMOVE LEADING AND TRAILING WS
                    parts = re.split(r"\s",line,1) 

                    #GET RID OF EXTRA SPACES
                    ordinal= parts[0].strip()
                    ordinal= ordinal.rstrip('.')
                    ordinal= ordinal.rstrip(')')

                    #GET RID OF EXTRA SPACES
                    if len(parts) == 2:
                        content = parts[1].strip()

                    extra=""

                    if "other" in content.lower() and "specify" in content.lower():
                        content = content.replace("_", "")
                        extra=' open=\"1\" openSize=\"'+openSize+'\" randomize=\"0\"'

                    #COMPOSE ROW
                    printPage += "  <row label=\"r%s\" value=\"%s\"%s>%s</row>\n" % (ordinal,ordinal, extra, content)

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeColsCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            #docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                input = re.sub("\t+", " ", input)
                #CLEAN UP SPACES
                input = re.sub("\n +\n", "\n\n", input)
                #CLEAN UP THE EXTRA LINE BREAKS
                input = re.sub("\n{2,}", "\n", input)
                input = fixUniCode(input)
                input = input.strip().split("\n")
                #start from output = to fill this class
                for x in range(0,len(input)):
                    input[x] = re.sub("^[a-zA-Z0-9]{1,2}[\.:\)][ \t]+", "\n", input[x])
                    input[x] = re.sub(r"^([0-9]{1,3})[\t\s.:)]([a-zA-Z0-9\s\'\"]+)$", r"\2<br/> \1", input[x])
                count = 0
                for x in input:
                    if "other" in input[count].strip().lower() and "specify" in input[count].strip().lower():
                        input[count] = input[count].strip().replace("_", "")
                        extra=' open=\"1\" openSize=\"10\" randomize=\"0\"'
                        printPage += "  <col label=\"c%s\"%s>%s</col>\n" % (str(count+1), extra, input[count].strip())
                        count += 1
                    else:
                        extra = ''

                        printPage += "  <col label=\"c%s\"%s>%s</col>\n" % (str(count+1), extra, input[count].strip())
                        count += 1

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeColsMatchLabelCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            #docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                input = fixUniCode(input)
                input = re.sub("\t+", " ", input)
                #CLEAN UP SPACES
                input = re.sub("\n +\n", "\n\n", input)
                #CLEAN UP THE EXTRA LINE BREAKS
                input = re.sub("\n{2,}", "\n", input)
                input = input.strip().split("\n")
                count = 0
                for line in input:
                     line = line.strip()
                     #SPLIT ON WHITESPACE -- REMOVE LEADING AND TRAILING WS
                     parts = re.split(r"\s",line,1) 

                     #GET RID OF EXTRA SPACES
                     ordinal= parts[0].strip()
                     ordinal= ordinal.rstrip('.')
                     ordinal= ordinal.rstrip(')')

                     #GET RID OF EXTRA SPACES
                     if len(parts) == 2: 
                       content = parts[1].strip()

                     extra=""

                     if "other" in content.lower() and "specify" in content.lower():
                       content = content.replace("_", "")
                       extra=' open=\"1\" openSize=\"10\" randomize=\"0\"'

                     #COMPOSE ROW
                     if ordinal[0].isalpha() and (len(parts) == 2):
                       printPage += "  <col label=\"%s\"%s>%s</col>\n" % (ordinal, extra, content)
                     elif ordinal[0].isdigit():
                       printPage += "  <col label=\"c%s\"%s>%s</col>\n" % (ordinal, extra, content)
                     else:
                       count += 1
                       printPage += "  <col label=\"c%s\"%s>%s</col>\n" % (str(count), extra, line)

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeColsMatchValueCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            #docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                input = re.sub("\t+", " ", input)
                #CLEAN UP SPACES
                input = re.sub("\n +\n", "\n\n", input)
                #CLEAN UP THE EXTRA LINE BREAKS
                input = re.sub("\n{2,}", "\n", input)
                input = fixUniCode(input)
                input = input.strip().split("\n")

                for line in input:
                     line = line.strip()
                     #SPLIT ON WHITESPACE -- REMOVE LEADING AND TRAILING WS
                     parts = re.split(r"\s",line,1) 

                     #GET RID OF EXTRA SPACES
                     ordinal= parts[0].strip()
                     ordinal= ordinal.rstrip('.')
                     ordinal= ordinal.rstrip(')')

                     #GET RID OF EXTRA SPACES 
                     content = parts[1].strip()

                     extra=""

                     if "other" in content.lower() and "specify" in content.lower():
                       content = content.replace("_", "")
                       extra=' open=\"1\" openSize=\"10\" randomize=\"0\"'

                     #COMPOSE COLUMN
                     printPage += "  <col label=\"c%s\" value=\"%s\"%s>%s</col>\n" % (ordinal,ordinal, extra, content)

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeChoicesCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                input = fixUniCode(input)
                input = input.strip().split("\n")

                for x in range(0,len(input)):
                    input[x] = re.sub("^[a-zA-Z0-9]{1,2}[\.:\)][ \t]+", "\n", input[x])
                count = 0
                for x in input:
                    printPage += "  <choice label=\"ch%s\">%s</choice>\n" % (str(count+1), input[count].strip())
                    count += 1
            self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeCasesCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                input = fixUniCode(input)
                while '\n\n' in input:
                    input = input.replace('\n\n', '\n')
                input = input.strip().split("\n")

                for x in range(0,len(input)):
                    input[x] = re.sub("^[a-zA-Z0-9]{1,2}[\.:\)][ \t]+", "\n", input[x])
                count = 0
                for x in input:
                    printPage += "  <case label=\"r%s\" cond=\"\">%s</case>\n" % (str(count+1), input[count].strip())
                    count += 1
                printPage += "  <case label=\"r%s\" cond=\"1\">UNDEFINED</case>" % (str(count+1))
            self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeGroupsCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel)
                input = fixUniCode(input)
                input = input.strip().split("\n")

                for x in range(0,len(input)):
                    input[x] = re.sub("^[a-zA-Z0-9]{1,2}[\.:\)][ \t]+", "\n", input[x])
                for x in range(len(input)):
                    printPage += "  <group label=\"g" + str(x+1) + "\">" + re.sub(r"^[a-zA-Z0-9]+(\.|:)|^[a-zA-Z0-9]+[a-zA-Z0-9]+(\.|:)", "", input[x]).strip() + "</group>\n"
            self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e

class makeLoopBlockCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel).strip()
                input = re.sub(r'<(radio|checkbox|text|textarea|block|number|float|select|html)(.*) label="([^"]*)"',r'<\1\2 label="\3_[loopvar: label]"', input)
                
                printPage = """
<loop label="" vars="" title=" " suspend="0">

    <block label="">

    %s

    </block>
    <looprow label="" cond="">
        <loopvar name=""></loopvar>
    </looprow>

</loop>

            """ % input

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e


class makeSwitchCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:
            sels = self.view.sel()
            for sel in sels:
                
                vrange = self.view.substr(sel).strip("\n").split("\n")
               
                for i in range(len(vrange)):

                    if "<row" in vrange[i]:
                        this1 = "row"
                        that1 = "col"
                        this2 = "r"
                        that2 = "c"
                    elif "<col" in vrange[i]:
                        this1 = "col"
                        that1 = "row"
                        this2 = "c"
                        that2 = "r"
                    vrange[i] = re.sub("(<|\/)" + this1, r'\1' + that1, vrange[i])
                    vrange[i] = re.sub('label="%s' % this2, 'label="%s' % that2, vrange[i])

                vrange = "\n".join(vrange)
                self.view.replace(edit,sel, vrange)
        except Exception, e:
            print e

class makeCommentCommand(sublime_plugin.TextCommand):
    def run (self,edit):
        try:

            sels = self.view.sel()
            input = ''
            docType =  returnContext(self)
            #print self.view.settings()
            for sel in sels:
                printPage = ''
                input = self.view.substr(sel).strip()
                input = fixUniCode(input)
                input = input.replace("\n", "<br/>\n")
                printPage = "<html label=\"\" where=\"survey\">%s</html>" % input

                self.view.replace(edit,sel, printPage)
        except Exception, e:
            print e


