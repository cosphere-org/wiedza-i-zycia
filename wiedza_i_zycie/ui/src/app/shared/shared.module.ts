import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EditionsDetalisNavComponent } from './editions-detalis-nav/editions-detalis-nav.component'
import { NavigationComponent } from './navigation/navigation.component'

import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module'

@NgModule({
  declarations: [EditionsDetalisNavComponent, NavigationComponent],
  imports: [
    CommonModule,
    SharedDependenciesModule,
  ]
})
export class SharedModule { }
