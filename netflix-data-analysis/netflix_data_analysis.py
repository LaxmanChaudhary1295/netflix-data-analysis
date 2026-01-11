import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("D:\\Data Science\\Python Programing\\Python Library - Matplotlib\\netflix_titles.csv")


#Q1
num_rows, num_col = df.shape
print("No.of rows",num_rows)
print("No.of columns",num_col)
print(df.columns)

#Q2

total_rows = df.shape[0]
missing_percentage = (df.isnull().sum() / total_rows)*100
missing_percentage = missing_percentage[missing_percentage>0].sort_values(ascending=False)

print(missing_percentage)

#Q3

Fill_Missing_Values = df.fillna(
    {
        "director": "Unknown",
        "cast": "Not Available",
        "country": "Unknown"
    }
)
print(Fill_Missing_Values)

#Q4

df["date_added"] = pd.to_datetime(df["date_added"], errors ="coerce")
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month
print(df[["date_added", "year_added", "month_added"]].head())

#Q5

type_counts = df["type"].value_counts()

type_percentage =(type_counts/type_counts.sum())*100
print(type_counts)
print(type_percentage)

plt.bar(type_counts.index,type_counts.values, width = 0.5,color ="orange")
plt.xlabel("Count Type")
plt.ylabel("Count Percentage")
plt.title("Movies & TV shows count")
plt.grid(linestyle = ":",linewidth = 0.5)
plt.tight_layout()
plt.savefig("Movies & TV shows count.png", dpi = 250, bbox_inches ="tight")
plt.show()

#Q6

titles_added_per_year =df["date_added"].value_counts().sort_index()
print(titles_added_per_year)

max_year = titles_added_per_year.idxmax()
max_counts =titles_added_per_year.max()

print("Year with highest content addition:",max_year)
print("Number of titles added:",max_counts)

plt.bar(titles_added_per_year.index,titles_added_per_year.values)
plt.xlabel("Year")
plt.ylabel("N.of Titles Added")
plt.title("Containt Added over Years")
plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("Containt Added over Years.png", dpi = 250, bbox_inches ="tight")
plt.show()

#Q7

content_added_per_month = df["date_added"].value_counts().sort_index()
print(content_added_per_month)

max_month = content_added_per_month.idxmax()
max_counts = content_added_per_month.max()
print("Highest content add in which month:",max_month)


#Q8

rating_count = df["rating"].value_counts()
print(rating_count)

top5_rating = rating_count.head(5)
print(top5_rating)

# Netflix audiance more focus on 18+ Shows and less focus on pg shows

#Q9

countries = df["country"].dropna()
countries = countries.str.split(",")

country_count = countries.value_counts()
top_10_countirs = country_count.head(10)
print(top_10_countirs)

#Q10

top_5_countries = (
    df["country"]
    .dropna()
    .str.split(", ")
    .explode()
    .str.strip()
    .value_counts()
    .head(5)
    .index
)

country_type_df = df[["country", "type"]].dropna(subset=["country"])
country_type_df["country"] = country_type_df["country"].str.split(", ")
country_type_df = country_type_df.explode("country")
country_type_df["country"] = country_type_df["country"].str.strip()
country_type_df = country_type_df[country_type_df["country"].isin(top_5_countries)]
country_vs_type = (
    country_type_df
    .groupby(["country", "type"])
    .size()
    .unstack(fill_value=0)
)
print(country_vs_type)

#Q11

india_usa_df=df[["country","type"]].dropna(subset =["country"])
india_usa_df = india_usa_df[india_usa_df["country"].isin(["India", "United States"])]

total_content = india_usa_df["country"].value_counts()
print("Total Content:", total_content)

movies_tv_ratio_df = (india_usa_df.
                      groupby(["country","type"]).
                      size()
                      .unstack(fill_value=0))
print("\nMovies vs Tv Shows:\n", movies_tv_ratio_df)

movies_tv_ratio_df.plot(kind="bar", figsize=(6,4))
plt.xlabel("country")
plt.ylabel("Number of Titles")
plt.title("India vs USA: Movies vs TV Shows")
plt.xticks(rotation = 0)
plt.tight_layout()
plt.savefig("India vs USA.png", dpi = 250, bbox_inches ="tight")
plt.show()

#Q12

genre = df["listed_in"].dropna().str.split(",").explode().str.strip()
genre_count = genre.value_counts()
top_10_most_common_genres = genre_count.head(10)
print("Most Common Genre:\n",top_10_most_common_genres)


#Q13

genre = df[["listed_in","type"]].dropna(subset =["listed_in"])
genre["listed_in"] = genre["listed_in"].str.split(",")
genre =genre.explode("listed_in")
genre["listed_in"]= genre["listed_in"].str.strip()

top_5_genre = genre["listed_in"].value_counts().head(5).index
genre = genre[genre["listed_in"].isin(top_5_genre)]

movies_tv_show_count = (genre.groupby(["listed_in","type"]).size().unstack(fill_value=0))
print("\nMovies Count v/s Tv Shows Count\n", movies_tv_show_count)

movies_tv_show_count.plot(kind="bar", figsize=(6,4))
plt.xlabel("Genre")
plt.ylabel("Movies Count v/s Tv Shows Count")
plt.title("Genre: Movies Count v/s Tv Shows Count")
plt.xticks(rotation = 90)
plt.tight_layout()
plt.savefig("Movies Count vs Tv Shows Count.png", dpi = 250, bbox_inches ="tight")
plt.show()


#Q14

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
gerne_year =df[["listed_in","date_added"]].dropna(subset=["listed_in","date_added"])
gerne_year["year_added"] =gerne_year["date_added"].dt.year

gerne_year["listed_in"]=(gerne_year["listed_in"]
                         .str.split(",")
                         .explode("listed_in")
                         .str.strip())
top_3_gernes = gerne_year["listed_in"].value_counts().head(3).index

gerne_year = gerne_year[gerne_year["listed_in"].isin(top_3_gernes)]

gerne_trend =( gerne_year.groupby(["year_added","listed_in"]).size().unstack(fill_value=0).sort_index())
print("Gerne Evolution Over Time:\n",gerne_trend)

gerne_trend.plot(kind="bar",figsize=(6,4))
plt.title("Genre Evolution Over Time")
plt.tight_layout()
plt.savefig("Genre Evolution Over Time.png", dpi = 250, bbox_inches ="tight")
plt.show()


#Q15

Movie_Duration = df[df["type"]=="Movie"].copy()

Movie_Duration["duration_minutes"] = (
    Movie_Duration["duration"].str.extract(r"(\d+)").astype(float)
)

avg_duration = Movie_Duration["duration_minutes"].mean()
print("Average Movie Duration (in minutes):", round(avg_duration,2))

longest_movie = Movie_Duration.loc[Movie_Duration["duration_minutes"].idxmax()]
print("Longest Movie:")
print(longest_movie[["title","duration"]])

shortest_movie = Movie_Duration.loc[Movie_Duration["duration_minutes"].idxmin()]
print("Shortest Movie:")
print(shortest_movie[["title","duration"]])

#Q16

tv_df = df[df["type"].str.strip().str.lower() == "tv show"].copy()

tv_df["num_seasons"] = (
    tv_df["duration"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(float)
)

tv_df = tv_df.dropna(subset=["num_seasons"])

max_seasons = tv_df["num_seasons"].max()
highest_season_shows = tv_df[tv_df["num_seasons"] == max_seasons]

print("Highest number of seasons:", max_seasons)
print("\nShows with highest seasons:")
print(highest_season_shows[["title", "num_seasons"]])

average_seasons = tv_df["num_seasons"].mean()
print("\nAverage number of seasons:", round(average_seasons, 2))

#Q17 

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

movies_df = df[
    (df["type"].str.lower() == "movie") &
    (df["date_added"].notna())
].copy()

movies_df["duration_minutes"] = (
    movies_df["duration"]
    .astype(str)
    .str.extract(r"(\d+)")
    .astype(float)
)

movies_df = movies_df.dropna(subset=["duration_minutes"])

movies_df["year_added"] = movies_df["date_added"].dt.year

duration_trend = (
    movies_df
    .groupby("year_added")["duration_minutes"]
    .mean()
    .sort_index()
)

print("Average Movie Duration Over Years:\n", duration_trend)

duration_trend.plot(kind="bar", figsize=(6,4))
plt.xlabel("Year")
plt.ylabel("Duration")
plt.xticks(rotation = 45)
plt.title("Average Movie Duration Over Years")
plt.tight_layout()
plt.savefig("Average Movie Duration Over Years.png", dpi = 250, bbox_inches ="tight")
plt.show()

#Q18

director = df[["director","type"]].dropna(subset=["director"])
director["director"] = director["director"].str.split(",").explode("director").str.strip()

movies_director = director[director["type"]=="Movie"]

top_10_movie_directors = (
    movies_director["director"]
    .value_counts()
    .head(10)
)

print("Top 10 Directors(Movies):\n",top_10_movie_directors)

tv_show_director = director[director["type"]=="TV Show"]
top_10_tv_shows_directors = (
    tv_show_director["director"]
    .value_counts()
    .head(10)
)

print("Top 10 Directors(TV Show):\n",top_10_tv_shows_directors)

fig, ax = plt.subplots(1, 2, figsize=(14, 5))


top_10_movie_directors.plot(
    kind="bar",
    ax=ax[0]
)
ax[0].set_title("Top 10 Directors (Movies)")
ax[0].set_xlabel("Directors")
ax[0].set_ylabel("Number of Movies")
ax[0].tick_params(axis="x", rotation=90)

top_10_tv_shows_directors.plot(
    kind="bar",
    ax=ax[1]
)
ax[1].set_title("Top 10 Directors (TV Shows)")
ax[1].set_xlabel("Directors")
ax[1].set_ylabel("Number of TV Shows")
ax[1].tick_params(axis="x", rotation=90)

plt.tight_layout()
plt.savefig("Top 10 Directors.png", dpi = 250, bbox_inches ="tight")
plt.show()



#Q19 

actor = df["cast"].dropna().str.split(",").explode().str.strip()

top_10_actors = actor.value_counts().head(10)
print("Top 10 actors based on appearances:\n", top_10_actors)

top_10_actors.plot(kind="barh", figsize=(6,4))
plt.xlabel("Appears")
plt.ylabel("Acorts")
plt.xticks(rotation =0)
plt.tight_layout()
plt.title("Top 10 actors based on appearances")
plt.savefig("Top 10 actors based on appearances.png", dpi = 250, bbox_inches ="tight")
plt.show()

#Q20

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
strategy = df[df["date_added"].notna()].copy()

strategy["year_added"] = strategy["date_added"].dt.year

movies_tv_trend = (
    strategy.groupby(["year_added","type"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

print("\nMovies vs TV Shows added per year:\n", movies_tv_trend)

movies_tv_trend.plot(kind="bar", figsize=(6,4))
plt.xlabel("Year")
plt.ylabel("Movies & TV Show")
plt.xticks(rotation=90)
plt.title("Netflix is shifting focus from Movies to TV Shows over time")
plt.tight_layout()
plt.savefig("Netflix is shifting focus from Movies to TV Shows over time.png", dpi = 250, bbox_inches ="tight")
plt.show()

#Q21

df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")
content_df = df[df["date_added"].notna() & df["rating"].notna()].copy()
content_df["year_added"] = content_df["date_added"].dt.year

family_ratings = ["G", "PG", "TV-G", "TV-PG", "TV-Y", "TV-Y7"]
mature_ratings = ["PG-13", "R", "NC-17", "TV-14", "TV-MA"]

def categorize_rating(rating):
    if rating in family_ratings:
        return "Family"
    elif rating in mature_ratings:
        return "Mature"
    else:
        return "Other"

content_df["content_category"] = content_df["rating"].apply(categorize_rating)

category_trend = (
    content_df
    .groupby(["year_added", "content_category"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
)

print("Family vs Mature Content Over Time:\n", category_trend)

category_trend.plot(kind="bar", figsize=(6,4))
plt.xlabel("Year")
plt.ylabel("No.of Titles Added")
plt.xticks(rotation = 90)
plt.title("Family vs Mature Content Trend on Netflix")
plt.tight_layout()
plt.savefig("Family vs Mature Content Trend on Netflix.png", dpi = 250, bbox_inches ="tight")
plt.show()