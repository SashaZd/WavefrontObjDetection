from Parser import Parser


file_name = 'Chair.obj.txt'
parsedObj = Parser(file_name)
print parsedObj.f[len(parsedObj.f)-1]
