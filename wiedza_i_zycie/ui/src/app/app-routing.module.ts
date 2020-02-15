import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { EditionsComponent } from './editions';
import { ArticlesComponent } from './articles';
import { MainViewComponent } from './main-view/main-view.component';
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
    path: 'articles',
    component: ArticlesComponent
  },
  {
    path: 'wiedza-i-zycie',
    component: MainViewComponent
  },
  {
    path: '**',
    component: PageNotFoundComponent
  },
];

export const AppRoutes = RouterModule.forRoot(routes);
