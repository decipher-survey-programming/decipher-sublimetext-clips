import sublime, sublime_plugin

class SelectToEndoflineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        for s in self.view.sel():
            caretPos = s.begin()
            self.view.sel().add(sublime.Region(caretPos, self.view.line(caretPos).end()))

class SelectToBegoflineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        caretPos = self.view.sel()[0].begin()
        self.view.sel().add(sublime.Region(caretPos, self.view.line(caretPos).begin()))

class SelectToNextCursorCommand(sublime_plugin.TextCommand):
    def run(self, edit):
            caretPos = self.view.sel()[0].begin()
            endPos = self.view.line(self.view.sel()[1].end()).end()
            self.view.sel().add(sublime.Region(caretPos, endPos))

class SelectToEndBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        caretPos = self.view.sel()[0].begin()
        endPos = self.view.line(self.view.sel()[0].end()).end()
        check = self.view.substr(sublime.Region(endPos+1,endPos+2))
        
        while check != '\n' and check !='':
            self.view.sel().add(sublime.Region(caretPos,self.view.line(endPos+1).end()))
            endPos = self.view.line(self.view.sel()[0].end()).end()
            check = self.view.substr(sublime.Region(endPos+1,endPos+2))

class SelectToStartBlockCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        caretPos = self.view.sel()[0].begin()
        endPos = self.view.line(self.view.sel()[0].begin()).begin()
        check = self.view.substr(sublime.Region(endPos-1,endPos-2))
        
        while check != '\n' and check !='':
            self.view.sel().add(sublime.Region(caretPos,self.view.line(endPos-1).begin()))
            endPos = self.view.line(self.view.sel()[0].begin()).begin()
            check = self.view.substr(sublime.Region(endPos-1,endPos-2))

