import { createReducer, on } from '@ngrx/store';
import { 
    increment,
    edit_search_field,
 } from './main-wiz.actions';

export const initialState = 0;
export const searchField = '';

const _counterReducer = createReducer(initialState,
  on(increment, state => state + 1),
);

export function counterReducer(state, action) {
  return _counterReducer(state, action);
}

//////////////////////////////////////////////////// 

const _searchReducer = createReducer(searchField,
    on(edit_search_field, state => this.state),
  );
  
  export function searchReducer(state, action) {
    return _counterReducer(state, action);
  }