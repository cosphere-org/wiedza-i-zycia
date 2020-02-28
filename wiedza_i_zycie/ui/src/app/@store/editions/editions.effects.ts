import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Action, Store } from '@ngrx/store';
import { Actions, Effect, ofType } from '@ngrx/effects';
import { Observable, of } from 'rxjs';
import { catchError, map, mergeMap, switchMap, filter, tap, withLatestFrom } from 'rxjs/operators';

import { AppState } from '../app-state';
import { EditionsActions } from './editions.actions';
import { Edition } from './editions.model';

@Injectable()
export class EditionsEffects {
  @Effect()
  onBulkReadEditions$: Observable<Action> = this.actions$.pipe(
    ofType<EditionsActions.BulkReadEditions>(EditionsActions.Type.BULK_READ_EDITIONS),
    switchMap(action => {
      return this.http.get('/assets/editions.json').pipe(
        tap(editions => {
          // np. tutaj byśmy mogli uruchomic progress bar!
          console.log('pokaż progress bar');
        }),
        map((editions: Edition[]) => new EditionsActions.BulkReadEditionsSuccess({ editions })),
        catchError(err => {
          return of(new EditionsActions.BulkReadEditionsError());
        })
      );
    })
  );

  constructor(
    private actions$: Actions,
    private store$: Store<AppState>,
    private http: HttpClient
  ) {}
}
