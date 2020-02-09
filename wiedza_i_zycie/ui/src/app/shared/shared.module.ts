import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { EditionsDetalisNavComponent } from './editions-detalis-nav/editions-detalis-nav.component'
import { NavigationComponent } from './navigation/navigation.component'
import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module';
import { PagesNavigationComponent } from './pages-navigation/pages-navigation.component';
import { SearchBoxComponent } from './search-box/search-box.component'

@NgModule({
  imports: [
    CommonModule,
    SharedDependenciesModule,
  ],
  declarations: [
    EditionsDetalisNavComponent,
    NavigationComponent,
    PagesNavigationComponent,
    SearchBoxComponent,
  ],
  exports: [
    EditionsDetalisNavComponent,
    NavigationComponent,
  ]
})
export class SharedModule { }
