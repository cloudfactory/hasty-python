from . import Dataset, Image, Label, LabelClass, LabelAttribute, LabelClassAttribute

class Utils:

    @staticmethod
    def copy_label_classes(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every label class in a project to an other
        '''
        dst_label_classes = LabelClass.fetch_all(API_class_dst, project_id_dst)
        dst_class_names = [i['name'] for i in dst_label_classes]

        label_classes = LabelClass.fetch_all(API_class_src, project_id_src)
        label_class_mapping = {}
        for label_class in label_classes:
            if label_class['name'] not in dst_class_names: # add label class if there is no name duplicates
                ret = LabelClass.copy(API_class_dst, project_id_dst, label_class)
                label_class_mapping[label_class['id']] = ret['id']

            else: # else, map the label class id to the existing one
                index = dst_class_names.index(label_class['name'])
                lab_class_id = dst_label_classes[index]['id']
                label_class_mapping[lab_class_id] = label_class['id']

        return label_class_mapping

    @staticmethod
    def copy_attribute_classes(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every attribute class in a project to an other
        '''
        dst_attribute_classes = LabelClassAttribute.fetch_all(API_class_dst, project_id_dst)
        dst_class_names = [i['name'] for i in dst_attribute_classes]

        attribute_classes = LabelClassAttribute.fetch_all(API_class_src, project_id_src)
        attribute_class_mapping = {}
        for attribute_class in attribute_classes:
            if attribute_class['name'] not in dst_class_names: # add attribute class if there is no name duplicates
                ret = LabelClassAttribute.copy(API_class_dst, project_id_dst, attribute_class)
                attribute_class_mapping[attribute_class['id']] = ret['id']

            else: # else, map the attribute class id to the existing one
                index = dst_class_names.index(attribute_class['name'])
                att_class_id = dst_attribute_classes[index]['id']
                attribute_class_mapping[att_class_id] = attribute_class['id']

        return attribute_class_mapping
        
    @staticmethod
    def copy_datasets(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every dataset in a project to an other
        '''
        dst_datasets = Dataset.fetch_all(API_class_dst, project_id_dst)
        dst_dataset_names = [i['name'] for i in dst_datasets]

        datasets = Dataset.fetch_all(API_class_src, project_id_src)
        dataset_mapping = {}
        for dataset in datasets:
            if dataset['name'] not in dst_dataset_names: # add dataset if there is no name duplicates
                ret = Dataset.copy(API_class_dst, project_id_dst, dataset)
                dataset_mapping[dataset['id']] = ret['id']
            
            else: # else, map the dataset id to the existing one
                index = dst_dataset_names.index(dataset['name'])
                dataset_id = dst_datasets[index]['id']
                dataset_mapping[dataset_id] = dataset['id']
        return dataset_mapping

    @staticmethod
    def copy_images(API_class_src, API_class_dst, project_id_src, project_id_dst, dataset_mapping):
        '''
        copy every image in a project to an other
        '''
        dst_images = Image.fetch_all(API_class_dst, project_id_dst) # can be long to fetch if the project is big
        dst_image_names = [i['name'] for i in dst_images]

        images = Image.fetch_all(API_class_src, project_id_src) # can be long to fetch if the project is big
        image_mapping = {}
        for image in images:
            if image['name'] not in dst_image_names: # add image if there is no name duplicates
                ret = Image.copy(API_class_dst, project_id_dst, image, dataset_mapping)
                image_mapping[image['id']] = ret['id']

            else: # else, map the image id to the existing one
                index = dst_image_names.index(image['name'])
                image_id = dst_images[index]['id']
                image_mapping[image_id] = image['id']

        return image_mapping
        
    @staticmethod
    def copy_labels(API_class_src, API_class_dst, project_id_src, project_id_dst, image_mapping, label_class_mapping):
        '''
        copy every label in a project to an other
        '''
        labels = Label.fetch_all(API_class_src, project_id_src)
        label_mapping = {}
        for label in labels:
            ret = Label.copy(API_class_dst, project_id_dst, label, image_mapping, label_class_mapping)
            label_mapping[label['id']] = ret['id']
        return label_mapping

    #TODO: add label attributes
    @staticmethod
    def copy_labels_attribute(API_class_src, API_class_dst, project_id_src, project_id_dst, label_mapping, attribute_class_mapping):
        '''
        copy every label attribute in a project to an other
        '''
        label_attributes = LabelAttribute.fetch_all(API_class_src, project_id_src, label_mapping)
        for label_attribute in label_attributes:
            label_id = label_attribute[0]
            for item_to_copy in label_attribute[label_id]:
                ret = LabelAttribute.copy(API_class_dst, project_id_dst, label_id, item_to_copy, attribute_class_mapping)
        return

    @staticmethod
    def copy_project(API_class_src, API_class_dst, project_id_src, project_id_dst):
        print("project in progress:", project_id_src)

        print("starting label class copy...")
        label_class_mapping = Utils.copy_label_classes(API_class_src, API_class_dst, project_id_src, project_id_dst)
        print("label class copy completed")

        print("starting attribute class copy...")
        attribute_class_mapping = Utils.copy_attribute_classes(API_class_src, API_class_dst, project_id_src, project_id_dst)
        print("attribute class copy completed")

        print("starting dataset copy...")
        dataset_mapping = Utils.copy_datasets(API_class_src, API_class_dst, project_id_src, project_id_dst)
        print("dataset copy completed")

        print("starting image copy...")
        image_mapping = Utils.copy_images(API_class_src, API_class_dst, project_id_src, project_id_dst, dataset_mapping)
        print("image copy completed")

        print("starting label copy...")
        label_mapping = Utils.copy_labels(API_class_src, API_class_dst, project_id_src, project_id_dst, image_mapping, label_class_mapping)
        print("label copy completed")

        print("starting label attribute copy...")
        Utils.copy_labels_attribute(API_class_src, API_class_dst, project_id_src, project_id_dst, label_mapping, attribute_class_mapping)
        print("label attribute copy completed")

        print("done")
        
    @staticmethod
    def merge_projects(API_class_src, API_class_dst, project_ids_src, project_id_dst):
        n_project = len(project_ids_src)
        for it in range(n_project):
            print(f"{it}/{n_project}")
            Utils.copy_project(API_class_src, API_class_dst, project_ids_src[it], project_id_dst)