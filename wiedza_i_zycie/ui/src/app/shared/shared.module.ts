import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module';
import { SearchBoxComponent } from './search-box/search-box.component';
import { MainToolbarComponent } from './main-toolbar/main-toolbar.component'


@NgModule({
  imports: [
    CommonModule,
    SharedDependenciesModule,
  ],
  declarations: [
    SearchBoxComponent,
    MainToolbarComponent,
  ],
  exports: [
    MainToolbarComponent,
  ]
})
export class SharedModule { }
