import docx2txt
import PyPDF2

def extract_text_from_file(file_obj, file_name):
    if file_name.endswith('.docx'):
        return docx2txt.process(file_obj)
    elif file_name.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file_obj)
        try:
            return '\n'.join([page.extract_text() or '' for page in reader.pages])
        except Exception:
            return ''
    elif file_name.endswith('.txt'):
        return file_obj.read().decode('utf-8')
    return ''
