import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module';
import { MainToolbarComponent } from './main-toolbar/main-toolbar.component'


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    SharedDependenciesModule,
  ],
  declarations: [
    MainToolbarComponent,
  ],
  exports: [
    MainToolbarComponent,
  ]
})
export class SharedModule { }
