import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { EditionsGridModule } from './editions-grid/editions-grid.module'
import {PageNotFoundComponent} from './page-not-found/page-not-found.component'

const routes: Routes = [
  { path: '',   redirectTo: '/editions', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];

@NgModule({
  imports: [
    RouterModule.forRoot(routes)
  ],
  exports: [RouterModule]
})
export class AppRoutingModule { }
