
import { EditionsState } from './editions/editions.state';
import { ArticlesState } from './articles/articles.state';

export interface AppState {
  readonly editions: EditionsState;
  readonly articles: ArticlesState;
}
