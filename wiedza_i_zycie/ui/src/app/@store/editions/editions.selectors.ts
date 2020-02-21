import { createSelector } from '@ngrx/store';

import { AppState } from '../app-state';
import { EditionsState } from './editions.state';

export namespace EditionsSelectors {
  export const editions = (state: AppState) => state.editions;

  export function getEditions() {
    return createSelector(
      editions,
      (state: EditionsState) => state
    );
  }
}
