from google.appengine.ext import ndb

def improve(result, identificador = ""): #explota con las sesiones
    result["id"] = identificador
    for key, value in result.iteritems():
        if type(value) is list:
            i = 0
            for item in value:
                if isinstance(item,ndb.Key):
                    value[i] = improve(item.get().to_dict())
                    value[i]["id"] = item.id()
                elif type(item) is not unicode:
                    value[i] = improve(result = item)
                i = i + 1
        if isinstance(value,ndb.Key):
            result[key] = improve(result[key].get().to_dict())
            result[key]["id"] = value.id()

    return result