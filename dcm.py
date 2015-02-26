import sublime_plugin, re

class MakeDcmCommand(sublime_plugin.TextCommand):

    def on_done(self, format):
        printPage = ''
        attrNum = 1
        level = 1
        restags = ''
        legend = ''

        dcmAtts = format.split('-')

        qLabel = str(dcmAtts[0])
        attrs = int(dcmAtts[1])
        columns = int(dcmAtts[2])
        tasks = int(dcmAtts[3])
        versions = int(dcmAtts[4])

        for sel in self.view.sel():
            nLs = self.view.split_by_newlines(sel)
            rowVs = [self.view.substr(x).strip() for x in nLs]
            rowVs = filter(None, rowVs)
            
        for x in rowVs:
            braks = re.search('\[([0-9]*)\]', x.strip())

            if braks:
                attrNum = braks.group(1)
                level = 1
                legend += "<res label=\"{question}_legend{attrNum}\">Legend {attrNum}</res>\n".format(question=qLabel, attrNum=attrNum)
            else:
                restags += "<res label=\""+qLabel+"_att{attrNum}_level{level}\">{resTag}</res>\n".format(attrNum=attrNum, level=level, resTag=x)
                level += 1


        dcm = self.make_question(qLabel, attrs, columns, tasks, versions, restags, legend)
        dcmExec = self.make_exec(qLabel)
        printPage += dcmExec + dcm

        self.view.replace(self.edit, sel, printPage)


    def preview(self, format):
        pass

    def cancel(self, format):
        pass



    def make_exec(self, qLabel):
        dcmExec = """
<exec when="init">
import csv
class DCM:
    def __init__(self, fname, delim="\t"):
        csvObj = csv.reader(open("%s/%s" % (gv.survey.path,fname)), delimiter=delim)
        
        dcm_concepts = []
        d = {}

        for i,row in enumerate(csvObj):
            if i:
                d["v%s_t%s_c%s" % (row[0],row[1],row[2])] = row[3:]

                if row[2] not in dcm_concepts:
                    dcm_concepts.append(row[2])

        self.concepts = sorted([ int(x) for x in dcm_concepts ])
        self.d = d

    def setupDCMItems(self, vt, prefix="1"):
        print "***** STAFF ONLY *****"
        print "***** DCM Matrix *****"
        print "Version_Task: %s" % vt

        
        for concept in self.concepts:
            attributes = self.d[ "%s_c%s" % (vt,concept) ]
            print "Concept %s: %s" % (concept,attributes)
            

            for i,attr in enumerate(attributes):
                p[ "concept%s_att%s" % (concept,i+1) ] = res[ "%s_att%s_level%s" % (prefix,i+1,attr) ]
                p[ "dcmLegend_att%s" % (i+1) ] = res[ "%s_legend%s" % (prefix,i+1) ]
</exec>

<exec when="init">
"""+qLabel+"""_dcm = DCM("design.txt")
</exec>
"""
        
        return dcmExec

            
    def make_question(self, qLabel, attrs, columns, tasks, versions, restags, legend):

        loopRows = ''
        for x in range(0,tasks):
            loopRows += """
            <looprow label=\""""+str(x+1)+"""\"><loopvar name="task">"""+str(x+1)+"""</loopvar></looprow>"""
        # legend = ''
        # for y in range(0,attrs):
        #     legend += """<res label=\""""+qLabel+"""_legend"""+str(y+1)+"""\">Legend """+str(y+1)+"""</res>
        #     """
        column  = ''
        for z in range(0, columns):
            column += """
            <col label=\"c"""+str(z+1)+"""\">Concept """+str(z+1)+"""</col>"""

        mainQuestion = """    
<quota overquota="noqual" sheet=\""""+qLabel+"""_DCM\"/>

<number label=\""""+qLabel+"""_Version\" size="3" optional="1" verify=\"range(1,"""+str(versions)+""")\" where="execute">
  <title>"""+qLabel+""" - DCM Version</title>
  <exec>
print p.markers
for x in p.markers:
  if \"/"""+qLabel+"""_DCM/ver_\" in x:
    """+qLabel+"""_Version.val = int(x.split("_")[-1])
    break
  </exec>
</number>
<suspend/>

"""+legend+"""

"""+restags+"""



<exec>p.startTime = time.time()</exec>

<loop label=\""""+qLabel+"""_dcm_loop\" vars="task" randomizeChildren="0">
  <title>"""+qLabel+""" - DCM Loop</title>
  <block label=\""""+qLabel+"""_dcm_block\" randomize="1">
    <radio label=\""""+qLabel+"""_[loopvar: task]\" optional="0" style="dcm"
      ss:questionClassNames=\""""+qLabel+"""_dcm\"
      dcm:attributes=\""""+str(attrs)+"""\"
      dcm:legend="1"
      dcm:top="Concepts"
      dcm:row="Select one option">
      <title>DCM Title [DCMcount]</title>
      <alt>DCM Task: [loopvar: task]</alt>
      <comment>Select one</comment>
      <exec>
"""+qLabel+"""_dcm.setupDCMItems( "v%s_t%s" % ("""+qLabel+"""_Version.val,"[loopvar: task]"),""""+qLabel+"""" )
p.DCMcount = "%d" % ("""+qLabel+"""_dcm_loop_expanded.order.index([loopvar: task]-1) + 1)
      </exec>
"""+column+"""
      <style name="question.header" mode="befor`e">
        <![CDATA[
          <style type="text/css">
/* add this only if you have scrollbars in IE7,8
div."""+qLabel+"""_dcm {
    overflow: hidden;
}
*/
."""+qLabel+"""_dcm tr.legend th.legend {
    font-weight: bold;
    width: auto;
}
."""+qLabel+"""_dcm th, ."""+qLabel+"""_dcm td {
    padding: 15px;
}
."""+qLabel+"""_dcm tr.dcm_even {
    background-color: #FFFFFF;
}
."""+qLabel+"""_dcm tr.dcm_odd {
    background-color: #EFEFEF;
}
."""+qLabel+"""_dcm td.dcm_legend {
    font-weight: bold;
    text-align: left;
    width: 120px;
}
."""+qLabel+"""_dcm tr.dcm_even td.dcm_item, ."""+qLabel+"""_dcm tr.dcm_odd td.dcm_item {
    text-align: center;
    width: 120px;
}
          </style>
        ]]>
      </style>

    </radio>
    <suspend/>
  </block>
  """+loopRows+"""      
  
</loop>

<float label=\""""+qLabel+"""_Timer\" size="15" where="execute">
  <title>"""+qLabel+""" - DCM Timer (Minutes)</title>
  <exec>"""+qLabel+"""_Timer.val = (time.time() - p.startTime) / 60.0</exec>
</float>

<exec>
del p.startTime
del p.DCMcount
</exec>
"""

        return mainQuestion


    def write_nstyles(self):
        tds = ''
        for i in range(0,self.concepts):
            tds += "    <td class='dcm_item'>${p.get('concept%d_att%d' % ([c.index+1 for c in p.get('shuffle-Col-%d' % this.uid) or this.cols]["+str(i)+"],x) )}</td>\n"


        nstyle='''
    ** attribute dcm:legend     type=int  desc="add left legend"
    ** attribute dcm:attributes type=int  desc="# of attributes"
    ** attribute dcm:top        type=text desc="text for the top legend"
    ** attribute dcm:row        type=text desc="text for the row radio legend"

    *dcm.top.legend:
    @if this.styles.dcm.legend
        <td class="dcm_legend">${this.styles.dcm.top or ""}</td>
    @endif

    *dcm/question.top-legend:
    @if this.styles.ss.colLegendHeight
    <tr class="legend top-legend${" GtTenColumns" if ec.colCount > 10 else ""} $(colError)" style="height:${this.styles.ss.colLegendHeight};">
    @else
    <tr class="legend top-legend${" GtTenColumns" if ec.colCount > 10 else ""} $(colError)">
    @endif
        [dcm.top.legend]
        $(left)
        $(legends)
        $(right)
    </tr>

    @for x in range(1,this.styles.dcm.attributes+1)
    <tr class="${'dcm_%s' % ['odd','even'][x % 2]}">
      @if this.styles.dcm.legend
        <td class="dcm_legend">${p.get('dcmLegend_att%d' % x)}</td>
      @endif
    '''+tds+'''
        </tr>
    @end
    <tbody>

    *dcm.row.legend:
    @if this.styles.dcm.legend
        <td class="dcm_legend">${this.styles.dcm.row or ""}</td>
    @endif

    *dcm/question.row:
    @if this.styles.ss.rowHeight
    <tr class="$(style) colCount-$(colCount)" style="height:${this.styles.ss.rowHeight};">
    @else
    <tr class="$(style) colCount-$(colCount)">
    @endif
        [dcm.row.legend]
        $(left)
        $(elements)
        $(right)
    </tr>

        '''

    def run(self, edit, preview=True):
        self.edit = edit
        self.view.window().show_input_panel(
            "Please enter the desired params QLabel-attNum-columns-tasks-versions",
            '',
            self.on_done,  # on_done
            self.preview if preview else None,  # on_change
            self.cancel    # on_cancel
        )
