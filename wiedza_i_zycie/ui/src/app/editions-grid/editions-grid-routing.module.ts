import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

// import { HeroListComponent }    from './hero-list/hero-list.component';
// import { HeroDetailComponent }  from './hero-detail/hero-detail.component';

import { EditionsGridComponent } from './editions-grid/editions-grid.component';

const heroesRoutes: Routes = [
  { path: 'editions',  component: EditionsGridComponent },
];

@NgModule({
  imports: [
    RouterModule.forChild(heroesRoutes)
  ],
  exports: [
    RouterModule
  ]
})
export class HeroesRoutingModule { }