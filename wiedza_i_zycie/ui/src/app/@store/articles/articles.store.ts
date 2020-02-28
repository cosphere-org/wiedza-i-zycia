import { Injectable } from '@angular/core';
import { Store, select } from '@ngrx/store';

import { AppState } from '../app-state';
import { ArticlesActions } from './articles.actions';
import { ArticlesSelectors } from './articles.selectors';
import { ArticlesState } from './articles.state';

@Injectable({
  providedIn: 'root'
})
export class ArticlesStore {
  constructor(private store$: Store<AppState>) {}

  state$ = this.store$.pipe(select(ArticlesSelectors.getEditions()));

  bulkReadEditions(articles?: []): void {
    this.store$.dispatch(new ArticlesActions.BulkReadArticles({ articles }));
  }

}
