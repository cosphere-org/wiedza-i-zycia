import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';

import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module';
import { ToolbarComponent } from './toolbar/toolbar.component'


@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    SharedDependenciesModule,
  ],
  declarations: [
    ToolbarComponent,
  ],
  exports: [
    ToolbarComponent,
  ]
})
export class SharedModule { }
