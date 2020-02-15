import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ArticleCardComponent } from './article-card/article-card.component';
import { ArticleGridComponent } from './article-grid/article-grid.component';
import { ArticleDetalisComponent } from './article-detalis/article-detalis.component';
import { ArticlesComponent } from './articles.component'
import { WizDataService } from 'src/app/wiz-data.service';
import { SharedModule } from 'src/app/shared/shared.module'
import { RouterModule } from '@angular/router'
import { SharedDependenciesModule } from '../shared-dependencies/shared-dependencies.module'

@NgModule({
  imports: [
    CommonModule,
    SharedDependenciesModule,
    SharedModule,
    RouterModule,
  ],
  providers: [
    WizDataService,
  ],
  declarations: [
    ArticleCardComponent, 
    ArticleGridComponent, 
    ArticleDetalisComponent, 
    ArticlesComponent
  ],
  exports: [
    ArticlesComponent
  ]
})
export class ArticlesModule { }
