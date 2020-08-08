
import { ArticlesActions } from './articles.actions';
import { ArticlesState } from './articles.state';

const initState: ArticlesState = {

  allArticles: [],
  filteredArticles: [],
  selectedArticle: null,

};

export function articlesReducer(state: ArticlesState = initState, action: ArticlesActions.Actions) {

  switch (action.type) {

    case ArticlesActions.Type.BULK_READ_ARTICLES:

      return {
        ...state,
        allArticles: action.payload.articles
      };

    default:
      return { ...state };
  }
}
