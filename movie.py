
import streamlit as st 
import streamlit.components.v1 as stc
import pandas as pd
import re
import requests
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

HTML_BANNER = """
    <div style="background-color:#6DC4FF;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Movie Recommendation </h1>
    </div>
    """
ratings = pd.read_csv('../dsMovie/rating.csv')
movies = pd.read_csv('../dsMovie/movie.csv')
links = pd.read_csv('../dsMovie/link.csv')

x = ratings['userId'].value_counts()>500
y = x[x].index

ratings = ratings[ratings['userId'].isin(y)]
movie_details = movies.merge(ratings,on = 'movieId')
movie_details.drop(columns=['timestamp'], inplace=True)
number_rating = movie_details.groupby('title')['rating'].count().reset_index()
number_rating.rename(columns={'rating':'number of rating'},inplace=True)

df = movie_details.merge(number_rating,on='title')
df = df[df['number of rating']>=50]
df.drop_duplicates(['title','userId'],inplace=True)
df.drop(columns=['number of rating'], inplace=True)
df['rating']=df['rating'].astype(int)

movie_pivot=df.pivot_table(columns='userId',index='title',values='rating')
movie_pivot.fillna(0,inplace=True)

from scipy.sparse import csr_matrix
movie_sparse=csr_matrix(movie_pivot)

from sklearn.neighbors import NearestNeighbors
model=NearestNeighbors(n_neighbors=7,algorithm='brute',metric='cosine')

model.fit(movie_sparse)

df.drop(columns=['genres','userId','rating'],inplace=True)
df.drop_duplicates(inplace=True)

df1 = df.copy()
ti = []
for i in df1['title']:
	ti.append(i.split(' (')[0])
df1['title'] = ti

distances,suggestions = model.kneighbors(movie_pivot.iloc[540,:].values.reshape(1,-1))
df = movie_details.merge(number_rating,on='title')

def recommend(movie_name):

	movie_id = df1[df1['title'] == movie_name].drop_duplicates('title')['movieId'].values[0]
	distances,suggestions = model.kneighbors(movie_pivot.iloc[movie_id,:].values.reshape(1,-1))

	for i in range(len(suggestions)):
		return(movie_pivot.index[suggestions[i]])

def main():
	
	stc.html(HTML_BANNER)
	df = pd.read_csv("movie.csv")

	movies_title_list = df['title'].tolist()

	movie_choice = st.selectbox("Select Movie Title Recommend Movies", movies_title_list)
	movie_choice = re.sub(r'\([^)]*\)', '', movie_choice)
	movie_choice = movie_choice.strip()
	result = recommend(movie_choice)
	with st.beta_expander('Movies',expanded=False):
		st.dataframe(df.head(10))

		title = df[df['title'] == movie_choice]['title'].values
		genre = df[df['title'] == movie_choice]['genres'].values


	c1,c2,c3 = st.beta_columns([1,2,1])

	with c1:
		with st.beta_expander("Title"):
			for i in result:
				st.success(i)

	with c2:
		with st.beta_expander("Poster"):
			#st.image(img_link,use_column_with=True)
			#st.markdown("![Alt Text]"+URL)
			st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")
	
if __name__ == '__main__':
	main()
