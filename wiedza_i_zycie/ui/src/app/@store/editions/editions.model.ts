
export interface Edition {
  date: string;
  image: string;
  table_of_contents: {
    sub_title: string;
    title: string;
  }[];
  url: string;
  articles: {
    title: string;
    author: string;
    date: string;
    image: string;
    paragraphs: string[];
    url: string;
  }[];
}
