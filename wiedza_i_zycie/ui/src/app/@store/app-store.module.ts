import { NgModule } from '@angular/core';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';

import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { editionsReducer } from './editions/editions.reducer';
import { articlesReducer } from './articles/articles.reducer';
import { EditionsEffects } from './editions/editions.effects';

@NgModule({
  declarations: [],
  imports: [
    StoreModule.forRoot({
      editions: editionsReducer,
      articles: articlesReducer,
    }),
    EffectsModule.forRoot([
      EditionsEffects,
    ]),
    StoreDevtoolsModule.instrument({
      maxAge: 50
    })
  ]
})
export class AppStoreModule {}
