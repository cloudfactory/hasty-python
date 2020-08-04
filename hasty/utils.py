from __future__ import absolute_import, division, print_function

from . import Dataset, Image, Label, LabelClass, LabelAttribute, Attribute


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
            if label_class['name'] not in dst_class_names:
                # add label class if there is no name duplicates
                ret = LabelClass.copy(API_class_dst,
                                      project_id_dst,
                                      label_class)
                label_class_mapping[label_class['id']] = ret['id']

            else:
                # else, map the label class id to the existing one
                index = dst_class_names.index(label_class['name'])
                lab_class_id = dst_label_classes[index]['id']
                label_class_mapping[label_class['id']] = lab_class_id

        return label_class_mapping

    @staticmethod
    def copy_attributes(API_class_src, API_class_dst, project_id_src, project_id_dst):
        '''
        copy every attribute in a project to an other
        '''
        dst_attributes = Attribute.fetch_all(API_class_dst, project_id_dst)
        dst_names = [i['name'] for i in dst_attributes]

        attributes = Attribute.fetch_all(API_class_src, project_id_src)
        attribute_mapping = {}
        for attribute in attributes:
            if attribute['name'] not in dst_names:
                # add attribute class if there is no name duplicates
                ret = Attribute.copy(API_class_dst,
                                     project_id_dst,
                                     attribute)
                attribute_mapping[attribute['id']] = ret['id']

            else:
                # else, map the attribute class id to the existing one
                index = dst_names.index(attribute['name'])
                att_class_id = dst_attributes[index]['id']
                attribute_mapping[attribute['id']] = att_class_id

        return attribute_mapping

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
            if dataset['name'] not in dst_dataset_names:
                # add dataset if there is no name duplicates
                ret = Dataset.copy(API_class_dst,
                                   project_id_dst,
                                   dataset)
                dataset_mapping[dataset['id']] = ret['id']

            else:
                # else, map the dataset id to the existing one
                index = dst_dataset_names.index(dataset['name'])
                dataset_id = dst_datasets[index]['id']
                dataset_mapping[dataset['id']] = dataset_id
        return dataset_mapping

    @staticmethod
    def copy_images(API_class_src, API_class_dst, project_id_src, project_id_dst,
                    dataset_mapping):
        '''
        copy every image in a project to an other
        '''
        dst_images = Image.fetch_all(API_class_dst, project_id_dst)  # can be long to fetch if the project is big
        dst_image_names = [i['name'] for i in dst_images]

        images = Image.fetch_all(API_class_src, project_id_src)  # can be long to fetch if the project is big
        image_mapping = {}
        for image in images:
            if image['name'] not in dst_image_names:
                # add image if there is no name duplicates
                ret = Image.copy(API_class_dst,
                                 project_id_dst,
                                 image,
                                 dataset_mapping)
                image_mapping[image['id']] = ret['id']

            else:
                # else, map the image id to the existing one
                index = dst_image_names.index(image['name'])
                image_id = dst_images[index]['id']
                image_mapping[image['id']] = image_id

        return image_mapping

    @staticmethod
    def copy_labels(API_class_src, API_class_dst, project_id_src, project_id_dst,
                    image_mapping, label_class_mapping):
        '''
        copy every label in a project to an other
        '''
        label_batches = Label.fetch_all(API_class_src, project_id_src, image_mapping)
        label_mapping = {}
        for label_batch in label_batches:
            ret = Label.copy(API_class_dst,
                             project_id_dst,
                             label_batch,
                             image_mapping,
                             label_class_mapping)
            for label, item in zip(label_batch, ret['items']):
                label_mapping[label['id']] = item['id']
        return label_mapping

    @staticmethod
    def copy_project_batch(API_class_src, API_class_dst, project_id_src, project_id_dst, batch_size=100, base_offset=0):
        '''
        copy every label class, attribute, dataset, images and labels from a project to an other
        not supported: set attribute classes, set attribute value, create image tags, set image tags
        '''
        label_class_mapping = Utils.copy_label_classes(API_class_src, API_class_dst, project_id_src, project_id_dst)
        attribute_mapping = Utils.copy_attributes(API_class_src, API_class_dst, project_id_src, project_id_dst)
        dataset_mapping = Utils.copy_datasets(API_class_src, API_class_dst, project_id_src, project_id_dst)

        n = Image.get_total_items(API_class_src, project_id_src)

        for offset in range(base_offset, n+1, batch_size):
            image_mapping = {}
            image_batch = Image.list(API_class_src, project_id_src, offset=offset, limit=batch_size)['items']
            for image in image_batch:
                try:
                    new_images = Image.copy(API_class_dst,
                                            project_id_dst,
                                            image,
                                            dataset_mapping)

                    image_mapping[image['id']] = new_images['id']

                    labels = Label.fetch_all_image(API_class_src, project_id_src, image['id'])
                    new_labels = Label.copy(API_class_dst, project_id_dst, labels, image_mapping, label_class_mapping)

                except KeyError:
                    print("a request has failed")
                except Exception as e:
                    print(e)

    @staticmethod
    def merge_projects(API_class_src, API_class_dst, project_ids_src, project_id_dst):
        n_project = len(project_ids_src)
        for it in range(n_project):
            print(f"{it+1}/{n_project}")
            Utils.copy_project_batch(API_class_src, API_class_dst, project_ids_src[it], project_id_dst)
