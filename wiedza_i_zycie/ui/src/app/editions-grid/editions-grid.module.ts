import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { EditionsCardComponent } from './editions-card/editions-card.component';
import { EditionDetalisComponent } from './edition-detalis/edition-detalis.component'
import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module'

import { MatCardModule } from '@angular/material/card';

@NgModule({
  declarations: [EditionsCardComponent, EditionDetalisComponent],
  imports: [
    CommonModule,
    SharedDependenciesModule,
    MatCardModule,
  ]
})
export class EditionsGridModule { }
