import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { EditionsDetalisNavComponent } from './editions-detalis-nav/editions-detalis-nav.component'
import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module';
import { PagesNavigationComponent } from './pages-navigation/pages-navigation.component';
import { SearchBoxComponent } from './search-box/search-box.component';
import { MainToolbarComponent } from './main-toolbar/main-toolbar.component'


@NgModule({
  imports: [
    CommonModule,
    SharedDependenciesModule,
  ],
  declarations: [
    EditionsDetalisNavComponent,
    PagesNavigationComponent,
    SearchBoxComponent,
    MainToolbarComponent,
  ],
  exports: [
    EditionsDetalisNavComponent,
    PagesNavigationComponent,
    MainToolbarComponent,
  ]
})
export class SharedModule { }
