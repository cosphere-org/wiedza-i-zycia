import { NgModule } from '@angular/core';
import { StoreModule } from '@ngrx/store';
import { EffectsModule } from '@ngrx/effects';

import { StoreDevtoolsModule } from '@ngrx/store-devtools';
import { editionsReducer } from './editions/editions.reducer';

@NgModule({
  declarations: [],
  imports: [
    StoreModule.forRoot({
      editions: editionsReducer,
    }),
    EffectsModule.forRoot([]),
    StoreDevtoolsModule.instrument({
      maxAge: 50
    })
  ]
})
export class AppStoreModule {}
