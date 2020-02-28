
import { Article } from './articles.model';

export interface ArticlesState {

  allArticles: Article[];

  filteredArticles: Article[];

  selectedArticles: Article;
}
