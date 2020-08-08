import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { EditionsComponent } from './editions';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

const routes: Routes = [
  { path: '',
    redirectTo: '/editions',
    pathMatch: 'full'
  },
  {
    path: 'editions',
    component: EditionsComponent
  },
  {
    path: '**',
    component: PageNotFoundComponent
  },
];

export const AppRoutes = RouterModule.forRoot(routes);
