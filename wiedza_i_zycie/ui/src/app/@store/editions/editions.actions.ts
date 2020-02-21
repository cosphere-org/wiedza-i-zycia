import { Action } from '@ngrx/store';

export namespace EditionsActions {
  export enum Type {
    BULK_READ_EDITIONS = '[EDITIONS] Bulk Read Editions',
  }

  export class BulkReadEditions implements Action {
    readonly type = Type.BULK_READ_EDITIONS;

    constructor(public payload: { query?: string }) {}
  }

  export type Actions =
    | BulkReadEditions;
}
