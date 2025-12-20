from app.backend.app.src.models.articles_to_dict import pdf_to_dict

file_path = '../../../datasets/статья 1.pdf'

article_dict = pdf_to_dict(file_path)
print(article_dict)