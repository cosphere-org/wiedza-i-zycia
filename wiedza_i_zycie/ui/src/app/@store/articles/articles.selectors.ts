import { createSelector } from '@ngrx/store';

import { AppState } from '../app-state';
import { ArticlesState } from './articles.state';

export namespace ArticlesSelectors {
  export const articles = (state: AppState) => state.articles;

  export function getEditions() {
    return createSelector(
      articles,
      (state: ArticlesState) => state
    );
  }
}
