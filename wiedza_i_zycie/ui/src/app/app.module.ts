import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AppRoutes } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { LayoutModule } from '@angular/cdk/layout';
import { FlexLayoutModule } from '@angular/flex-layout/';
import { HttpClientModule } from '@angular/common/http';

import { SharedDependenciesModule} from './shared-dependencies/shared-dependencies.module';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component'
import { EditionsModule } from './editions/editions.module';
import { SharedModule } from './@shared/shared.module'

import { AppStoreModule } from '@store';

@NgModule({
  declarations: [
    AppComponent,
    PageNotFoundComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    LayoutModule,
    FlexLayoutModule,
    FormsModule,
    HttpClientModule,
    SharedDependenciesModule,
    EditionsModule,
    SharedModule,
    AppRoutes,
    AppStoreModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
