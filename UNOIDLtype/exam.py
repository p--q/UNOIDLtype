import ast
class ReversePrintNodeTransformer(ast.NodeTransformer):
    def visit_Name(self, node):
        if node.id == 'print':
            name = ast.Name(id='reverse_print', ctx=ast.Load())
            return ast.copy_location(name, node)
        return node

def reverse_print(s):
    print(''.join(reversed(s)))
    
source = """
print(s)
"""

s = 'hello world'  
tree = ast.parse(source, mode="exec") 
# code = compile(ReversePrintNodeTransformer().visit(tree), '<string>', 'exec')


cl = ReversePrintNodeTransformer()
cl.visit(tree)
code = compile(tree, '<string>', 'exec')
# exec(code)
# s = 'revese print'
# exec(code)



# temp = {}
exec(code, globals())

func.__name__


# def exam():
# #     print = replaceExam
#     print("プリント")
#     p = replaceExam
# #     replaceExam("引数")
#     p("引数")
#     
# def replaceExam(txt):
#     print(txt)
#     print("置換後")
#     
#     
# 
# 
# exam()
# 
# src = " どういう意味？"
# if src.startswith((' ','\t')):
#     src = 'if 1:\n' + src
# print(src)