import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EditionsCardComponent } from './editions-card/editions-card.component';
import { EditionDetalisComponent } from './edition-detalis/edition-detalis.component'
import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module'

import { WizDataService } from './wiz-data.service'

@NgModule({
  declarations: [EditionsCardComponent, EditionDetalisComponent],
  imports: [
    CommonModule,
    SharedDependenciesModule,
  ],
  providers: [
    WizDataService,
  ]
})
export class EditionsGridModule { }
