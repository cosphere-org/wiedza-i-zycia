
import { ArticlesActions } from './articles.actions';
import { ArticlesState } from './articles.state';

const initState: ArticlesState = {

  allArticles: [],
  filteredArticles: [],
  selectedArticle: null,

};

export function editionsReducer(state: ArticlesState = initState, action: ArticlesActions.Actions) {

  switch (action.type) {

    case ArticlesActions.Type.BULK_READ_ARTICLES:

      if (action.payload.articles) {
        return {
          ...state,
          filteredEditions: [
            {
              articles: [],
              table_of_contents: [],
              date: '08/2011',
              image: 'b178bc2b0799bfd8194d6ad90f5a912d.jpg',
              url: 'https://www.wiz.pl/10,82.html'
            },
          ]
        };
      }

      return {
        ...state,
        filteredEditions: [
          {
            articles: [],
            table_of_contents: [],
            date: '08/2011',
            image: 'b178bc2b0799bfd8194d6ad90f5a912d.jpg',
            url: 'https://www.wiz.pl/10,82.html'
          },
          {
            articles: [],
            table_of_contents: [],
            date: '01/2018',
            image: '408379496eeb6132bb6ffc6e9dfa9395.jpg',
            url: 'https://www.wiz.pl/10,254.html'
          },
        ]
      };

    default:
      return { ...state };
  }
}
