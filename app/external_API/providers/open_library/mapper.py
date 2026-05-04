from app.external_API.providers.open_library.dto import ExternalBookDTO,WorkBookDTO


class OpenLibraryMapper:

    @staticmethod
    def map_search_result(item: dict) -> ExternalBookDTO:
        return ExternalBookDTO(
            title=item.get("title", ""),
            authors=item.get("author_name", []),
            first_publish_year=item.get("first_publish_year"),
            isbn=item.get("isbn", []),
            language=item.get("language", []),
            cover_id=item.get("cover_i"),
            work_id=item.get("key")
        )
    
    @staticmethod
    def map_work_result(item: dict) -> WorkBookDTO:
        return WorkBookDTO(
            work_id=item.get("key", "").split("/")[-1],
            title=item.get("title", ""),

            description=(
                item.get("description", {}).get("value")
                if isinstance(item.get("description"), dict)
                else item.get("description")
            ),

            subjects=item.get("subjects") or [],

            author_keys=[
                a["author"]["key"].split("/")[-1]
                for a in item.get("authors", [])
                if "author" in a
            ],

            cover_ids=item.get("covers") or [],
        )