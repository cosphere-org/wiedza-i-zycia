
import { EditionsActions } from './editions.actions';
import { EditionsState } from './editions.state';

const initState: EditionsState = {

  allEditions: [],
  filteredEditions: [],
  selectedEdition: null,
  setProgressBar: false,

};

export function editionsReducer(state: EditionsState = initState, action: EditionsActions.Actions) {

  let query;
  let filteredEditions;

  switch (action.type) {

    case EditionsActions.Type.BULK_READ_EDITIONS_SUCCESS:

      return {
        ...state,
        allEditions: action.payload.editions,
        filteredEditions: action.payload.editions.slice(0, 30)
      };

    case EditionsActions.Type.FILTER_EDITIONS:

      if (state.allEditions.length === 0) {
        return state;
      }

      filteredEditions = state.allEditions.filter(edition => {

        const articles = edition.articles.map(a => {
          const paragraphs = a.paragraphs.join('\n');

          return `${a.title} \n ${paragraphs}`;
        });

        const editionText = articles.join('\n');

        return new RegExp(action.payload.query, 'gim').test(editionText);
      });

      return {
        ...state,
        filteredEditions: filteredEditions.slice(0, 30)
      };

    case EditionsActions.Type.RUN_PROGRESS_BAR:

      return {
        ...state,
        setProgressBar: true
      }

    case EditionsActions.Type.STOP_PROGRESS_BAR:

      return {
        ...state,
        setProgressBar: false
      }
      
    case EditionsActions.Type.SUBSET_EDITIONS:

      return {
        ...state,
        filteredEditions: state.allEditions.slice(action.payload.start, action.payload.end)
      }

    default:
      return { ...state };
  }
}
