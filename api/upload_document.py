from inverted_index import getInvertedIndex
import shutil
import os

def upload_document(file, workingDirectory='./temp'):
	print('Saving file locally...')
	if not os.path.exists(workingDirectory):
		os.makedirs(workingDirectory)

	filePath = f'{workingDirectory}/{file.filename}'
	file.save(filePath)
	print(f'File "{file.filename}" saved successfully at "{filePath}"!')

	print('Loading file...')
	invertedIndex = getInvertedIndex()
	invertedIndex.loadDocument(filePath)
	print(f'File {file.filename} loaded successfully!')

	print('Cleaning up...')
	try:
		shutil.rmtree(workingDirectory)
	except OSError as e:
		print("Error: %s - %s." % (e.filename, e.strerror))
	print('Working directory removed!')
