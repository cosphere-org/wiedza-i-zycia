import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module'
import { EditionsCardComponent } from './editions-card/editions-card.component';
import { EditionDetalisComponent } from './edition-detalis/edition-detalis.component'
import { EditionsGridComponent } from './editions-grid/editions-grid.component'
import { EditionsComponent } from './editions.component'
import { WizDataService } from 'src/app/wiz-data.service';
import { SharedModule } from 'src/app/@shared/shared.module'
import { RouterModule } from '@angular/router'

@NgModule({
  imports: [
    CommonModule,
    SharedDependenciesModule,
    SharedModule,
    RouterModule,
  ],
  providers: [
    WizDataService,
  ],
  declarations: [
    EditionsCardComponent,
    EditionDetalisComponent,
    EditionsGridComponent,
    EditionsComponent,
  ],
  exports: [
    EditionsComponent,
  ]
})
export class EditionsModule { }
