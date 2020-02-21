import { Component } from '@angular/core';

import { Store, select } from '@ngrx/store';
import { Observable } from 'rxjs';
import { edit_search_field } from 'src/app/main-wiz.actions';

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.scss']
})
export class SearchBoxComponent  {

  constructor(private store: Store<{ shField: string }>) {
    this.shField$ = store.pipe(select('shField'));
  }

  editField() {
    // console.log(this.shField$);
    console.log(this)
    // this.form.value
    this.store.dispatch(edit_search_field());
  }

  shField$: Observable<string>;


}
