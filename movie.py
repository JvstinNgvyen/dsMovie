# core pkg
import streamlit as st 
import streamlit.components.v1 as stc

# EDA Pkgs
import pandas as pd

HTML_BANNER = """
    <div style="background-color:#6DC4FF;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Movie Recommendation </h1>
    </div>
    """


def main():
	
	stc.html(HTML_BANNER)
	df = pd.read_csv("movie.csv")

	# with st.beta_expander("Title"):
	# 	mytext = st.text_area("Type Here")
	# 	st.write(mytext)
	# 	st.success("Hello")

	# st.dataframe(df)
	movies_title_list = df['title'].tolist()

	movie_choice = st.selectbox("Select Movie Title To See Top 5 Recommend Movies", movies_title_list)
	with st.beta_expander('Movies DF',expanded=False):
		st.dataframe(df.head(10))

		# Filter
		#img_link = df[df['title'] == movie_choice]['img_link'].values[0]
		title = df[df['title']== movie_choice]['title'].values
		genre = df[df['title']== movie_choice]['genres'].values

	# Layout
		# st.write(img_link)
		# st.image(img_link)
	c1,c2,c3 = st.beta_columns([1,2,1])

	with c1:
		with st.beta_expander("Title"):
			st.success(title)

	#with c2:
	#	with st.beta_expander("Image"):
	#		st.image(img_link,use_column_with=True)


if __name__ == '__main__':
	main()
