import language_tool_python
tool = language_tool_python.LanguageTool('en-US')

string = 'A sentence with a error in the Hitchhiker’s Guide tot he Galaxy'

new = tool.correct(string)
print(new)
tool.close()