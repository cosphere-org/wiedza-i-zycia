
import { EditionsActions } from './editions.actions';
import { EditionsState } from './editions.state';

const initState: EditionsState = {

  allEditions: [],
  filteredEditions: [],
  selectedEdition: null,

};

export function editionsReducer(state: EditionsState = initState, action: EditionsActions.Actions) {

  switch (action.type) {

    case EditionsActions.Type.BULK_READ_EDITIONS:

      if (action.payload.query) {
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
